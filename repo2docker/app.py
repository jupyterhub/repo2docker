"""repo2docker: convert git repositories into jupyter-suitable docker images

Images produced by repo2docker can be used with Jupyter notebooks standalone
or with BinderHub.

Usage:

    python -m repo2docker https://github.com/you/your-repo
"""
import argparse
import json
import sys
import logging
import os
import pwd
import subprocess
import shutil
import tempfile
import time

import docker
from urllib.parse import urlparse
from docker.utils import kwargs_from_env
from docker.errors import DockerException
import escapism
from pythonjsonlogger import jsonlogger

from traitlets import Any, Dict, Int,  List, Unicode, default
from traitlets.config import Application

from . import __version__
from .buildpacks import (
    PythonBuildPack, DockerBuildPack, LegacyBinderDockerBuildPack,
    CondaBuildPack, JuliaBuildPack, BaseImage,
    RBuildPack, NixBuildPack
)
from . import contentproviders
from .utils import (
    ByteSpecification, is_valid_docker_image_name,
    validate_and_generate_port_mapping, chdir
)


class Repo2Docker(Application):
    """An application for converting git repositories to docker images"""
    name = 'jupyter-repo2docker'
    version = __version__
    description = __doc__

    @default('log_level')
    def _default_log_level(self):
        """The application's default log level"""
        return logging.INFO

    git_workdir = Unicode(
        None,
        config=True,
        allow_none=True,
        help="""
        Working directory to use for check out of git repositories.

        The default is to use the system's temporary directory. Should be
        somewhere ephemeral, such as /tmp.
        """
    )

    subdir = Unicode(
        '',
        config=True,
        help="""
        Subdirectory of the git repository to examine.

        Defaults to ''.
        """
    )

    cache_from = List(
        [],
        config=True,
        help="""
        List of images to try & re-use cached image layers from.

        Docker only tries to re-use image layers from images built locally,
        not pulled from a registry. We can ask it to explicitly re-use layers
        from non-locally built images by through the 'cache_from' parameter.
        """
    )

    buildpacks = List(
        [
            LegacyBinderDockerBuildPack,
            DockerBuildPack,
            JuliaBuildPack,
            NixBuildPack,
            RBuildPack,
            CondaBuildPack,
            PythonBuildPack,
        ],
        config=True,
        help="""
        Ordered list of BuildPacks to try when building a git repository.
        """
    )

    default_buildpack = Any(
        PythonBuildPack,
        config=True,
        help="""
        The default build pack to use when no other buildpacks are found.
        """
    )

    # Git is our content provider of last resort. This is to maintain the
    # old behaviour when git and local directories were the only supported
    # content providers. We can detect local directories from the path, but
    # detecting if something will successfully `git clone` is very hard if all
    # you can do is look at the path/URL to it.
    content_providers = List(
        [
            contentproviders.Local,
            contentproviders.Git,
        ],
        config=True,
        help="""
        Ordered list by priority of ContentProviders to try in turn to fetch
        the contents specified by the user.
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

        Only used when running, not during build process!

        Use a key-value pair, with the key being the volume source &
        value being the destination volume.

        Both source and destination can be relative. Source is resolved
        relative to the current working directory on the host, and
        destination is resolved relative to the working directory of the
        image - ($HOME by default)
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

        Should be a username that is not currently used by anything in the
        image, and should conform to the restrictions on user names for Linux.

        Defaults to username of currently running user, since that is the most
        common case when running repo2docker manually.
        """,
        config=True
    )

    @default('user_name')
    def _user_name_default(self):
        """
        Default user_name to current running user.
        """
        return pwd.getpwuid(os.getuid()).pw_name

    appendix = Unicode(
        config=True,
        help="""
        Appendix of Dockerfile commands to run at the end of the build.

        Can be used to customize the resulting image after all
        standard build steps finish.
        """
    )

    def fetch(self, url, ref, checkout_path):
        """Fetch the contents of `url` and place it in `checkout_path`.

        The `ref` parameter specifies what "version" of the contents should be
        fetched. In the case of a git repository `ref` is the SHA-1 of a commit.

        Iterate through possible content providers until a valid provider,
        based on URL, is found.
        """
        picked_content_provider = None
        for ContentProvider in self.content_providers:
            cp = ContentProvider()
            spec = cp.detect(url, ref=ref)
            if spec is not None:
                picked_content_provider = cp
                self.log.info("Picked {cp} content "
                              "provider.\n".format(cp=cp.__class__.__name__))
                break

        if picked_content_provider is None:
            self.log.error("No matching content provider found for "
                           "{url}.".format(url=url))

        for log_line in picked_content_provider.fetch(
                spec, checkout_path, yield_output=self.json_logs):
            self.log.info(log_line, extra=dict(phase='fetching'))

    def validate_image_name(self, image_name):
        """
        Validate image_name read by argparse

        Note: Container names must start with an alphanumeric character and
        can then use _ . or - in addition to alphanumeric.
        [a-zA-Z0-9][a-zA-Z0-9_.-]+

        Args:
            image_name (string): argument read by the argument parser

        Returns:
            unmodified image_name

        Raises:
            ArgumentTypeError: if image_name contains characters that do not
                               meet the logic that container names must start
                               with an alphanumeric character and can then
                               use _ . or - in addition to alphanumeric.
                               [a-zA-Z0-9][a-zA-Z0-9_.-]+
        """
        if not is_valid_docker_image_name(image_name):
            msg = ("%r is not a valid docker image name. Image name"
                   "must start with an alphanumeric character and"
                   "can then use _ . or - in addition to alphanumeric." % image_name)
            raise argparse.ArgumentTypeError(msg)
        return image_name

    def get_argparser(self):
        """Get arguments that may be used by repo2docker"""
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
            help=('If building a git url, which reference to check out. '
                  'E.g., `master`.')
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
            help=('Specify port mappings for the image. Needs a command to '
                  'run in the container.')
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

        argparser.add_argument(
            '--editable', '-E',
            dest='editable',
            action='store_true',
            help='Use the local repository in edit mode',
        )

        argparser.add_argument(
            '--appendix',
            type=str,
            help=self.traits()['appendix'].help,
        )

        argparser.add_argument(
            '--subdir',
            type=str,
            help=self.traits()['subdir'].help,
        )

        argparser.add_argument(
            '--version',
            dest='version',
            action='store_true',
            help='Print the repo2docker version and exit.'
        )

        argparser.add_argument(
            '--cache-from',
            action='append',
            default=[],
            help=self.traits()['cache_from'].help
        )

        return argparser

    def json_excepthook(self, etype, evalue, traceback):
        """Called on an uncaught exception when using json logging

        Avoids non-JSON output on errors when using --json-logs
        """
        self.log.error("Error during build: %s", evalue,
                       exc_info=(etype, evalue, traceback),
                       extra=dict(phase='failed'))

    def initialize(self, argv=None):
        """Init repo2docker configuration before start"""
        if argv is None:
            argv = sys.argv[1:]

        # version must be checked before parse, as repo/cmd are required and
        # will spit out an error if allowed to be parsed first.
        if '--version' in argv:
            print(self.version)
            sys.exit(0)

        args = self.get_argparser().parse_args(argv)

        if args.debug:
            self.log_level = logging.DEBUG

        self.load_config_file(args.config)
        if args.appendix:
            self.appendix = args.appendix

        self.repo = args.repo
        self.ref = args.ref
        # if the source exists locally we don't want to delete it at the end
        if os.path.exists(args.repo):
            self.cleanup_checkout = False
        else:
            self.cleanup_checkout = args.clean

        # user wants to mount a local directory into the container for
        # editing
        if args.editable:
            # the user has to point at a directory, not just a path for us
            # to be able to mount it. We might have content providers that can
            # provide content from a local `something.zip` file, which we
            # couldn't mount in editable mode
            if os.path.isdir(args.repo):
                self.volumes[os.path.abspath(args.repo)] = '.'
            else:
                self.log.error('Can not mount "{}" in editable mode '
                               'as it is not a directory'.format(args.repo),
                               extra=dict(phase='failed'))
                sys.exit(1)

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

        # check against self.run and not args.run as self.run is false on
        # --no-build
        if args.volumes and not self.run:
            # Can't mount if we aren't running
            print('To Mount volumes with -v, you also need to run the '
                  'container')
            sys.exit(1)

        for v in args.volumes:
            src, dest = v.split(':')
            self.volumes[src] = dest

        self.run_cmd = args.cmd

        if args.all_ports and not self.run:
            print('To publish user defined port mappings, the container must '
                  'also be run')
            sys.exit(1)

        if args.ports and not self.run:
            print('To publish user defined port mappings, the container must '
                  'also be run')
            sys.exit(1)

        if args.ports and not self.run_cmd:
            print('To publish user defined port mapping, user must specify '
                  'the command to run in the container')
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
            print('To specify environment variables, you also need to run '
                  'the container')
            sys.exit(1)

        if args.subdir:
            self.subdir = args.subdir

        if args.cache_from:
            self.cache_from = args.cache_from

        self.environment = args.environment

    def push_image(self):
        """Push docker image to registry"""
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
        self.log.info(f'Successfully pushed {self.output_image_spec}', extra=dict(phase='pushing'))

    def run_image(self):
        """Run docker container from built image

        and wait for it to finish.
        """
        container = self.start_container()
        self.wait_for_container(container)

    def start_container(self):
        """Start docker container from built image

        Returns running container
        """
        client = docker.from_env(version='auto')

        docker_host = os.environ.get('DOCKER_HOST')
        if docker_host:
            host_name = urlparse(docker_host).hostname
        else:
            host_name = '127.0.0.1'
        self.hostname = host_name

        if not self.run_cmd:
            port = str(self._get_free_port())
            self.port = port
            # To use the option --NotebookApp.custom_display_url
            # make sure the base-notebook image is updated:
            # docker pull jupyter/base-notebook
            run_cmd = [
                'jupyter', 'notebook',
                '--ip', '0.0.0.0',
                '--port', port,
                "--NotebookApp.custom_display_url=http://{}:{}".format(host_name, port),
            ]
            ports = {'%s/tcp' % port: port}
        else:
            # run_cmd given by user, if port is also given then pass it on
            run_cmd = self.run_cmd
            if self.ports:
                ports = self.ports
            else:
                ports = {}
        # store ports on self so they can be retrieved in tests
        self.ports = ports

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

        return container

    def wait_for_container(self, container):
        """Wait for a container to finish

        Displaying logs while it's running
        """

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
            if exit_code:
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
        """Start execution of repo2docker""" # Check if r2d can connect to docker daemon
        if self.build:
            try:
                api_client = docker.APIClient(version='auto',
                                              **kwargs_from_env())
            except DockerException as e:
                print("Docker client initialization error. Check if docker is"
                      " running on the host.")
                print(e)
                if self.log_level == logging.DEBUG:
                    raise e
                sys.exit(1)

        # If the source to be executed is a directory, continue using the
        # directory. In the case of a local directory, it is used as both the
        # source and target. Reusing a local directory seems better than
        # making a copy of it as it might contain large files that would be
        # expensive to copy.
        if os.path.isdir(self.repo):
            checkout_path = self.repo
        else:
            if self.git_workdir is None:
                checkout_path = tempfile.mkdtemp(prefix='repo2docker')
            else:
                checkout_path = self.git_workdir

        try:
            self.fetch(self.repo, self.ref, checkout_path)

            if self.subdir:
                checkout_path = os.path.join(checkout_path, self.subdir)
                if not os.path.isdir(checkout_path):
                    self.log.error('Subdirectory %s does not exist',
                                   self.subdir, extra=dict(phase='failure'))
                    sys.exit(1)

            with chdir(checkout_path):
                for BP in self.buildpacks:
                    bp = BP()
                    if bp.detect():
                        picked_buildpack = bp
                        break
                else:
                    picked_buildpack = self.default_buildpack()

                picked_buildpack.appendix = self.appendix

                self.log.debug(picked_buildpack.render(),
                               extra=dict(phase='building'))

                if self.build:
                    build_args = {
                        'NB_USER': self.user_name,
                        'NB_UID': str(self.user_id)
                    }
                    self.log.info('Using %s builder\n', bp.__class__.__name__,
                                  extra=dict(phase='building'))

                    for l in picked_buildpack.build(api_client, self.output_image_spec,
                        self.build_memory_limit, build_args, self.cache_from):
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
        finally:
            # Cheanup checkout if necessary
            if self.cleanup_checkout:
                shutil.rmtree(checkout_path, ignore_errors=True)

        if self.push:
            self.push_image()

        if self.run:
            self.run_image()
