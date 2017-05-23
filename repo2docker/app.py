import sys
import json
import os
import time
import logging
import uuid
import shutil
from pythonjsonlogger import jsonlogger


from traitlets.config import Application, LoggingConfigurable
from traitlets import Type, Bool, Unicode, Dict, List
import docker
from docker.utils import kwargs_from_env

import subprocess

from .detectors import BuildPack, PythonBuildPack, DockerBuildPack, CondaBuildPack
from .utils import execute_cmd


class Repo2Docker(Application):
    config_file = Unicode(
        'repo2docker_config.py',
        config=True,
        help="""
        Path to read traitlets configuration file from.
        """
    )

    repo = Unicode(
        '.',
        allow_none=True,
        config=True,
        help="""
        The git repository to clone.

        Could be a https URL, or a file path.
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

    aliases = Dict({
        'repo': 'Repo2Docker.repo',
        'ref': 'Repo2Docker.ref',
        'image': 'Repo2Docker.output_image_spec',
        'clean': 'Repo2Docker.cleanup_checkout',
        'f': 'Repo2Docker.config_file',
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

    def run(self):
        # HACK: Try to just pull this and see if that works.
        # if it does, then just bail.
        # WHAT WE REALLY WANT IS TO NOT DO ANY WORK IF THE IMAGE EXISTS
        client = docker.APIClient(version='auto', **kwargs_from_env())

        repo, tag = self.output_image_spec.split(':')
        try:
            for line in client.pull(
                    repository=repo,
                    tag=tag,
                    stream=True,
            ):
                progress = json.loads(line.decode('utf-8'))
                if 'error' in progress:
                    # pull failed, proceed to build
                    break
            else:
                # image exists, nothing to build
                return
        except docker.errors.ImageNotFound:
            # image not found, proceed to build
            pass


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

        # Build a progress setup for each layer, and only emit per-layer info every 1.5s
        layers = {}
        last_emit_time = time.time()
        for line in client.push(self.output_image_spec, stream=True):
            progress = json.loads(line.decode('utf-8'))
            if 'id' not in progress:
                continue
            if 'progressDetail' in progress and progress['progressDetail']:
                layers[progress['id']] = progress['progressDetail']
            else:
                layers[progress['id']] = progress['status']
            if time.time() - last_emit_time > 1.5:
                self.log.info('Pushing image', extra=dict(progress=layers, phase='pushing'))
                last_emit_time = time.time()

        if self.cleanup_checkout:
            shutil.rmtree(checkout_path)


