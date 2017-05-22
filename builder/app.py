import sys
import json
import os
import time
import logging
from pythonjsonlogger import jsonlogger


from traitlets.config import Application, LoggingConfigurable, Unicode, Dict, List
from traitlets import Type
import docker
from docker.utils import kwargs_from_env

import subprocess

from .detectors import BuildPack, PythonBuildPack, DockerBuildPack, CondaBuildPack
from .utils import execute_cmd


class Builder(Application):
    config_file = Unicode(
        'builder_config.py',
        config=True
    )

    build_name = Unicode(
        None,
        allow_none=True,
        config=True
    )

    source_url = Unicode(
        None,
        allow_none=True,
        config=True
    )

    source_ref = Unicode(
        'master',
        allow_none=True,
        config=True
    )

    output_image_spec = Unicode(
        None,
        allow_none=True,
        config=True
    )

    git_workdir = Unicode(
        "/tmp/git",
        config=True
    )

    buildpacks = List(
        None,
        [DockerBuildPack, CondaBuildPack, PythonBuildPack],
        config=True
    )

    aliases = Dict({
        'source': 'Builder.source_url',
        'ref': 'Builder.source_ref',
        'output': 'Builder.output_image_spec',
        'f': 'Builder.config_file',
        'n': 'Builder.build_name'
    })


    def fetch(self, url, ref, output_path):
        try:
            for line in execute_cmd(['git', 'clone', url, output_path]):
                self.log.info(line, extra=dict(phase='fetching'))
        except subprocess.CalledProcessError:
            self.log.error('Failed to clone repository!', extra=dict(phase='failed'))
            sys.exit(1)

        try:
            for line in execute_cmd(['git', '--git-dir', os.path.join(output_path, '.git'), 'reset', '--hard', ref]):
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

        output_path = os.path.join(self.git_workdir, self.build_name)
        self.fetch(
            self.source_url,
            self.source_ref,
            output_path
        )
        for bp_class in self.buildpacks:
            bp = bp_class()
            if bp.detect(output_path):
                self.log.info('Using %s builder', bp.name, extra=dict(phase='building'))
                bp.build(output_path, self.source_ref, self.output_image_spec)
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


if __name__ == '__main__':
    f = Builder()
    f.initialize()
    f.run()
