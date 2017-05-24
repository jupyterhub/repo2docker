"""repo2docker: convert git repositories into jupyter-suitable docker images

Images produced by repo2docker can be used with Jupyter notebooks standalone or via JupyterHub.

Usage:

    python -m repo2docker https://github.com/you/your-repo
"""
import sys
import json
import os
import time
import logging
import uuid
import shutil
from pythonjsonlogger import jsonlogger
import escapism


from traitlets.config import Application, LoggingConfigurable
from traitlets import Type, Bool, Unicode, Dict, List
import docker
from docker.utils import kwargs_from_env

import subprocess

from .detectors import BuildPack, PythonBuildPack, DockerBuildPack, CondaBuildPack
from .utils import execute_cmd
from . import __version__

class Repo2Docker(Application):
    name = 'jupyter-repo2docker'
    version = __version__
    description = __doc__

    config_file = Unicode(
        'repo2docker_config.py',
        config=True,
        help="""
        Path to read traitlets configuration file from.
        """
    )

    repo = Unicode(
        os.getcwd(),
        allow_none=True,
        config=True,
        help="""
        The git repository to clone.

        Could be a git URL or a file path.
        """
    )

    ref = Unicode(
        'master',
        allow_none=True,
        config=True,
        help="""
        The git ref in the git repository to build.

        Can be a tag, ref or branch.
        """
    )

    output_image_spec = Unicode(
        None,
        allow_none=True,
        config=True,
        help="""
        The spec of the image to build.

        Should be the same as the value passed to `-t` param of docker build.
        """
    )

    git_workdir = Unicode(
        "/tmp",
        config=True,
        help="""
        The directory to use to check out git repositories into.

        Should be somewhere ephemeral, such as /tmp
        """
    )

    buildpacks = List(
        Type(BuildPack),
        [DockerBuildPack, CondaBuildPack, PythonBuildPack],
        config=True,
        help="""
        Ordered list of BuildPacks to try to use to build a git repository.
        """
    )

    cleanup_checkout = Bool(
        True,
        config=True,
        help="""
        Set to True to clean up the checked out directory after building is done.

        Will only clean up after a successful build - failed builds will still leave their
        checkouts intact.
        """
    )

    push = Bool(
        False,
        config=True,
        help="""
        If the image should be pushed after it is built.
        """
    )

    run = Bool(
        True,
        config=True,
        help="""
        Run the image after it is built, if the build succeeds.

        DANGEROUS WHEN DONE IN A CLOUD ENVIRONMENT! ONLY USE LOCALLY!
        """
    )

    aliases = Dict({
        'repo': 'Repo2Docker.repo',
        'ref': 'Repo2Docker.ref',
        'image': 'Repo2Docker.output_image_spec',
        'f': 'Repo2Docker.config_file',
    })

    flags = Dict({
        'no-clean': ({'Repo2Docker': {'cleanup_checkout': False}}, 'Do not clean up git checkout'),
        'no-run': ({'Repo2Docker': {'run': False}}, 'Do not run built container image'),
        'push': ({'Repo2Docker': {'push': True}}, 'Push built image to a docker registry'),
    })

    def fetch(self, url, ref, checkout_path):
        try:
            for line in execute_cmd(['git', 'clone', url, checkout_path]):
                self.log.info(line, extra=dict(phase='fetching'))
        except subprocess.CalledProcessError:
            self.log.error('Failed to clone repository!', extra=dict(phase='failed'))
            sys.exit(1)

        try:
            for line in execute_cmd(['git', 'reset', '--hard', ref], checkout_path):
                self.log.info(line, extra=dict(phase='fetching'))
        except subprocess.CalledProcessError:
            self.log.error('Failed to check out ref %s', ref, extra=dict(phase='failed'))
            sys.exit(1)

    def initialize(self, *args, **kwargs):
        super().initialize(*args, **kwargs)
        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter()
        logHandler.setFormatter(formatter)
        # Need to reset existing handlers, or we repeat messages
        self.log.handlers = []
        self.log.addHandler(logHandler)
        self.log.setLevel(logging.INFO)
        self.load_config_file(self.config_file)

        if len(self.extra_args) == 1:
            # accept repo as a positional arg
            self.repo = self.extra_args[0]
        elif len(self.extra_args) > 1:
            print("%s accepts at most one positional argument." % self.name, file=sys.stderr)
            print("See python -m repo2docker --help for usage", file=sys.stderr)
            self.exit(1)

        if self.output_image_spec is None:
            # Attempt to set a sane default!
            # HACK: Provide something more descriptive?
            self.output_image_spec = escapism.escape(self.repo).lower() + ':' + self.ref.lower()


    def push_image(self):
        client = docker.APIClient(version='auto', **kwargs_from_env())
        # Build a progress setup for each layer, and only emit per-layer info every 1.5s
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
                self.log.info('Pushing image', extra=dict(progress=layers, phase='pushing'))
                last_emit_time = time.time()

    def run_image(self):
        client = docker.from_env(version='auto')
        port = self._get_free_port()
        container = client.containers.run(
            self.output_image_spec,
            ports={'%s/tcp' % port: port},
            detach=True,
            command=['jupyter', 'notebook', '--ip', '0.0.0.0', '--port', str(port)],
        )
        while container.status == 'created':
            time.sleep(0.5)
            container.reload()

        try:
            for line in container.logs(stream=True):
                self.log.info(line.decode('utf-8').rstrip(), extra=dict(phase='running'))
        finally:
            self.log.info('Stopping container...', extra=dict(phase='running'))
            container.kill()
            container.remove()

    def _get_free_port(self):
        """
        Hacky method to get a free random port on local host
        """
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        port = s.getsockname()[1]
        s.close()
        return port

    def image_exists(self):
        client = docker.from_env(version='auto')
        # HACK: Try to just pull this and see if that works.
        # if it does, then just bail.
        # WHAT WE REALLY WANT IS TO NOT DO ANY WORK IF THE IMAGE EXISTS
        try:
            image = client.images.pull(self.output_image_spec)
            return True
        except docker.errors.ImageNotFound:
            return False

    def start(self):
        if not self.image_exists():
            checkout_path = os.path.join(self.git_workdir, str(uuid.uuid4()))
            self.fetch(
                self.repo,
                self.ref,
                checkout_path
            )
            for bp_class in self.buildpacks:
                bp = bp_class()
                if bp.detect(checkout_path):
                    self.log.info('Using %s builder', bp.name, extra=dict(phase='building'))
                    bp.build(checkout_path, self.ref, self.output_image_spec)
                    break
            else:
                self.log.error('Could not figure out how to build this repository! Tell us?', extra=dict(phase='failed'))
                sys.exit(1)

            if self.cleanup_checkout:
                shutil.rmtree(checkout_path)

        if self.push:
            self.push_image()

        if self.run:
            self.run_image()



