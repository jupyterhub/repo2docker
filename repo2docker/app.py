"""repo2docker: convert git repositories into jupyter-suitable docker images

Images produced by repo2docker can be used with Jupyter notebooks standalone
or with BinderHub.

Usage:

    python -m repo2docker https://github.com/you/your-repo
"""
import sys
import json
import os
import time
import logging
import argparse
import tempfile
from pythonjsonlogger import jsonlogger
import escapism
import pwd


from traitlets.config import Application
from traitlets import Unicode, List, default, Any, Dict, Int
import docker
from docker.utils import kwargs_from_env
from docker.errors import DockerException

import subprocess

from .buildpacks import (
    PythonBuildPack, DockerBuildPack, LegacyBinderDockerBuildPack,
    CondaBuildPack, JuliaBuildPack, Python2BuildPack, BaseImage,
    RBuildPack
)
from .utils import execute_cmd, ByteSpecification, maybe_cleanup, is_valid_docker_image_name, validate_and_generate_port_mapping
from . import __version__



class Repo2Docker(Application):
    name = 'jupyter-repo2docker'
    version = __version__
    description = __doc__

    @default('log_level')
    def _default_log_level(self):
        return logging.INFO

    git_workdir = Unicode(
        None,
        config=True,
        allow_none=True,
        help="""
        Working directory to check out git repositories to.

        The default is to use the system's temporary directory. Should be
        somewhere ephemeral, such as /tmp.
        """
    )

    buildpacks = List(
        [
            LegacyBinderDockerBuildPack(),
            DockerBuildPack(),
            JuliaBuildPack(),
            CondaBuildPack(),
            Python2BuildPack(),
            RBuildPack(),
            PythonBuildPack()
        ],
        config=True,
        help="""
        Ordered list of BuildPacks to try to use to build a git repository.
        """
    )

    default_buildpack = Any(
        PythonBuildPack(),
        config=True,
        help="""
        The build pack to use when no buildpacks are found
        """
    )

    build_memory_limit = ByteSpecification(
        0,
        help="""
        Total memory that can be used by the docker image building process.

        Set to 0 for no limits.
        """,
        config=True
    )

    volumes = Dict(
        {},
        help="""
        Volumes to mount when running the container.

        Only used when running, not during build!

        Should be a key value pair, with the key being the volume source &
        value being the destination. Both can be relative - sources are
        resolved relative to the current working directory on the host,
        destination is resolved relative to the working directory of the image -
        ($HOME by default)
        """,
        config=True
    )

    user_id = Int(
        help="""
        UID of the user to create inside the built image.

        Should be a uid that is not currently used by anything in the image.
        Defaults to uid of currently running user, since that is the most
        common case when running r2d manually.

        Might not affect Dockerfile builds.
        """,
        config=True
    )

    @default('user_id')
    def _user_id_default(self):
        """
        Default user_id to current running user.
        """
        return os.geteuid()

    user_name = Unicode(
        'jovyan',
        help="""
        Username of the user to create inside the built image.

        Should be a username that is not currently used by anything in the image,
        and should conform to the restrictions on user names for Linux.

        Defaults to username of currently running user, since that is the most
        common case when running r2d manually.
        """,
        config=True
    )

    @default('user_name')
    def _user_name_default(self):
        """
        Default user_name to current running user.
        """
        return pwd.getpwuid(os.getuid()).pw_name

    def fetch(self, url, ref, checkout_path):
        try:
            for line in execute_cmd(['git', 'clone', url, checkout_path],
                                    capture=self.json_logs):
                self.log.info(line, extra=dict(phase='fetching'))
        except subprocess.CalledProcessError:
            self.log.error('Failed to clone repository!',
                           extra=dict(phase='failed'))
            sys.exit(1)

        if ref:
            try:
                for line in execute_cmd(['git', 'reset', '--hard', ref],
                                        cwd=checkout_path,
                                        capture=self.json_logs):
                    self.log.info(line, extra=dict(phase='fetching'))
            except subprocess.CalledProcessError:
                self.log.error('Failed to check out ref %s', ref,
                               extra=dict(phase='failed'))
                sys.exit(1)

    def validate_image_name(self, image_name):
        """
        Validate image_name read by argparse contains only lowercase characters

        Args:
            image_name (string): argument read by the argument parser

        Returns:
            unmodified image_name

        Raises:
            ArgumentTypeError: if image_name contains characters that are not lowercase
        """

        if not is_valid_docker_image_name(image_name):
            msg = "%r is not a valid docker image name. Image name can contain only lowercase characters." % image_name
            raise argparse.ArgumentTypeError(msg)
        return image_name

    def get_argparser(self):
        argparser = argparse.ArgumentParser()
        argparser.add_argument(
            '--config',
            default='repo2docker_config.py',
            help="Path to config file for repo2docker"
        )

        argparser.add_argument(
            '--json-logs',
            default=False,
            action='store_true',
            help='Emit JSON logs instead of human readable logs'
        )

        argparser.add_argument(
            'repo',
            help=('Path to repository that should be built. Could be '
                  'local path or a git URL.')
        )

        argparser.add_argument(
            '--image-name',
            help=('Name of image to be built. If unspecified will be '
                  'autogenerated'),
            type=self.validate_image_name
        )

        argparser.add_argument(
            '--ref',
            help='If building a git url, which ref to check out'
        )

        argparser.add_argument(
            '--debug',
            help="Turn on debug logging",
            action='store_true',
        )

        argparser.add_argument(
            '--no-build',
            dest='build',
            action='store_false',
            help=('Do not actually build the image. Useful in conjunction '
                  'with --debug.')
        )

        argparser.add_argument(
            '--build-memory-limit',
            help='Total Memory that can be used by the docker build process'
        )

        argparser.add_argument(
            'cmd',
            nargs=argparse.REMAINDER,
            help='Custom command to run after building container'
        )

        argparser.add_argument(
            '--no-run',
            dest='run',
            action='store_false',
            help='Do not run container after it has been built'
        )

        argparser.add_argument(
            '--publish', '-p',
            dest='ports',
            action='append',
            help='Specify port mappings for the image. Needs a command to run in the container.'
        )

        argparser.add_argument(
            '--publish-all', '-P',
            dest='all_ports',
            action='store_true',
            help='Publish all exposed ports to random host ports.'
        )

        argparser.add_argument(
            '--no-clean',
            dest='clean',
            action='store_false',
            help="Don't clean up remote checkouts after we are done"
        )

        argparser.add_argument(
            '--push',
            dest='push',
            action='store_true',
            help='Push docker image to repository'
        )

        argparser.add_argument(
            '--volume', '-v',
            dest='volumes',
            action='append',
            help='Volumes to mount inside the container, in form src:dest',
            default=[]
        )

        argparser.add_argument(
            '--user-id',
            help='User ID of the primary user in the image',
            type=int
        )

        argparser.add_argument(
            '--user-name',
            help='Username of the primary user in the image',
        )

        argparser.add_argument(
            '--env', '-e',
            dest='environment',
            action='append',
            help='Environment variables to define at container run time',
            default=[]
        )

        return argparser

    def json_excepthook(self, etype, evalue, traceback):
        """Called on an uncaught exception when using json logging

        Avoids non-JSON output on errors when using --json-logs
        """
        self.log.error("Error during build: %s", evalue,
                       exc_info=(etype, evalue, traceback),
                       extra=dict(phase='failed'))

    def initialize(self):
        args = self.get_argparser().parse_args()

        if args.debug:
            self.log_level = logging.DEBUG

        self.load_config_file(args.config)

        if os.path.exists(args.repo):
            # Let's treat this as a local directory we are building
            self.repo_type = 'local'
            self.repo = args.repo
            self.ref = None
            self.cleanup_checkout = False
        else:
            self.repo_type = 'remote'
            self.repo = args.repo
            self.ref = args.ref
            self.cleanup_checkout = args.clean

        if args.json_logs:
            # register JSON excepthook to avoid non-JSON output on errors
            sys.excepthook = self.json_excepthook
            # Need to reset existing handlers, or we repeat messages
            logHandler = logging.StreamHandler()
            formatter = jsonlogger.JsonFormatter()
            logHandler.setFormatter(formatter)
            self.log = logging.getLogger("repo2docker")
            self.log.handlers = []
            self.log.addHandler(logHandler)
            self.log.setLevel(logging.INFO)
        else:
            # due to json logger stuff above,
            # our log messages include carriage returns, newlines, etc.
            # remove the additional newline from the stream handler
            self.log.handlers[0].terminator = ''
            # We don't want a [Repo2Docker] on all messages
            self.log.handlers[0].formatter = logging.Formatter(
                fmt='%(message)s'
            )

        if args.image_name:
            self.output_image_spec = args.image_name
        else:
            # Attempt to set a sane default!
            # HACK: Provide something more descriptive?
            self.output_image_spec = (
                'r2d' +
                escapism.escape(self.repo, escape_char='-').lower() +
                str(int(time.time()))
            )

        self.push = args.push
        self.run = args.run
        self.json_logs = args.json_logs

        self.build = args.build
        if not self.build:
            # Can't push nor run if we aren't building
            self.run = False
            self.push = False

        # check against self.run and not args.run as self.run is false on --no-build
        if args.volumes and not self.run:
            # Can't mount if we aren't running
            print("To Mount volumes with -v, you also need to run the container")
            sys.exit(1)

        for v in args.volumes:
            src, dest = v.split(':')
            self.volumes[src] = dest

        self.run_cmd = args.cmd

        if args.all_ports and not self.run:
            print('To publish user defined port mappings, the container must also be run')
            sys.exit(1)

        if args.ports and not self.run:
            print('To publish user defined port mappings, the container must also be run')
            sys.exit(1)

        if args.ports and not self.run_cmd:
            print('To publish user defined port mapping, user must specify the command to run in the container')
            sys.exit(1)

        self.ports = validate_and_generate_port_mapping(args.ports)
        self.all_ports = args.all_ports

        if args.user_id:
            self.user_id = args.user_id
        if args.user_name:
            self.user_name = args.user_name

        if args.build_memory_limit:
            self.build_memory_limit = args.build_memory_limit

        if args.environment and not self.run:
            print("To specify environment variables, you also need to run the container")
            sys.exit(1)

        self.environment = args.environment

    def push_image(self):
        client = docker.APIClient(version='auto', **kwargs_from_env())
        # Build a progress setup for each layer, and only emit per-layer
        # info every 1.5s
        layers = {}
        last_emit_time = time.time()
        for line in client.push(self.output_image_spec, stream=True):
            progress = json.loads(line.decode('utf-8'))
            if 'error' in progress:
                self.log.error(progress['error'], extra=dict(phase='failed'))
                sys.exit(1)
            if 'id' not in progress:
                continue
            if 'progressDetail' in progress and progress['progressDetail']:
                layers[progress['id']] = progress['progressDetail']
            else:
                layers[progress['id']] = progress['status']
            if time.time() - last_emit_time > 1.5:
                self.log.info('Pushing image\n',
                              extra=dict(progress=layers, phase='pushing'))
                last_emit_time = time.time()

    def run_image(self):
        client = docker.from_env(version='auto')
        if not self.run_cmd:
            port = str(self._get_free_port())

            run_cmd = ['jupyter', 'notebook', '--ip', '0.0.0.0',
                       '--port', port]
            ports = {'%s/tcp' % port: port}
        else:
            # run_cmd given by user, if port is also given then pass it on
            run_cmd = self.run_cmd
            if self.ports:
                ports = self.ports
            else:
                ports = {}
        container_volumes = {}
        if self.volumes:
            api_client = docker.APIClient(
                version='auto',
                **docker.utils.kwargs_from_env()
            )
            image = api_client.inspect_image(self.output_image_spec)
            image_workdir = image['ContainerConfig']['WorkingDir']

            for k, v in self.volumes.items():
                container_volumes[os.path.abspath(k)] = {
                    'bind': v if v.startswith('/') else os.path.join(image_workdir, v),
                    'mode': 'rw'
                }

        container = client.containers.run(
            self.output_image_spec,
            publish_all_ports=self.all_ports,
            ports=ports,
            detach=True,
            command=run_cmd,
            volumes=container_volumes,
            environment=self.environment
        )
        while container.status == 'created':
            time.sleep(0.5)
            container.reload()

        try:
            for line in container.logs(stream=True):
                self.log.info(line.decode('utf-8'),
                              extra=dict(phase='running'))
        finally:
            container.reload()
            if container.status == 'running':
                self.log.info('Stopping container...\n',
                              extra=dict(phase='running'))
                container.kill()
            exit_code = container.attrs['State']['ExitCode']
            container.remove()
            sys.exit(exit_code)

    def _get_free_port(self):
        """
        Hacky method to get a free random port on local host
        """
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 0))
        port = s.getsockname()[1]
        s.close()
        return port


    def start(self):
        # Check if r2d can connect to docker daemon
        if self.build:
            try:
                client = docker.APIClient(version='auto',
                                          **kwargs_from_env())
                del client
            except DockerException as e:
                print("Docker client initialization error. Check if docker is running on the host.")
                print(e)
                if self.log_level == logging.DEBUG:
                    raise e
                sys.exit(1)

        if self.repo_type == 'local':
            checkout_path = self.repo
        else:
            if self.git_workdir is None:
                checkout_path = tempfile.mkdtemp(prefix='repo2docker')
            else:
                checkout_path = self.git_workdir

        # keep as much as possible in the context manager to make sure we
        # cleanup if things go wrong
        with maybe_cleanup(checkout_path, self.cleanup_checkout):
            if self.repo_type == 'remote':
                self.fetch(
                    self.repo,
                    self.ref,
                    checkout_path
                )

            os.chdir(checkout_path)
            picked_buildpack = self.default_buildpack

            for bp in self.buildpacks:
                if bp.detect():
                    picked_buildpack = bp
                    break

            self.log.debug(picked_buildpack.render(),
                           extra=dict(phase='building'))

            if self.build:
                build_args = {
                    'NB_USER': self.user_name,
                    'NB_UID': str(self.user_id)
                }
                self.log.info('Using %s builder\n', bp.__class__.__name__,
                              extra=dict(phase='building'))
                for l in picked_buildpack.build(self.output_image_spec, self.build_memory_limit, build_args):
                    if 'stream' in l:
                        self.log.info(l['stream'],
                                      extra=dict(phase='building'))
                    elif 'error' in l:
                        self.log.info(l['error'], extra=dict(phase='failure'))
                        sys.exit(1)
                    elif 'status' in l:
                            self.log.info('Fetching base image...\r',
                                          extra=dict(phase='building'))
                    else:
                        self.log.info(json.dumps(l),
                                      extra=dict(phase='building'))

        if self.push:
            self.push_image()

        if self.run:
            self.run_image()
