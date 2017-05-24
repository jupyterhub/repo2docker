import os
import sys
import subprocess

import docker

from traitlets import Unicode, Dict
from traitlets.config import LoggingConfigurable

import logging
from pythonjsonlogger import jsonlogger

from .utils import execute_cmd

here = os.path.abspath(os.path.dirname(__file__))

class BuildPack(LoggingConfigurable):
    name = Unicode()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # FIXME: Not sure why this needs to be repeated - shouldn't configuring Application be enough?
        logHandler = logging.StreamHandler()
        formatter = jsonlogger.JsonFormatter()
        logHandler.setFormatter(formatter)
        # Need to reset existing handlers, or we repeat messages
        self.log.handlers = []
        self.log.addHandler(logHandler)
        self.log.setLevel(logging.INFO)

    def detect(self, workdir):
        """
        Return True if app in workdir can be built with this buildpack
        """
        pass

    def build(self, workdir, ref, output_image_spec):
        """
        Run a command that will take workdir and produce an image ready to be pushed
        """
        pass


class DockerBuildPack(BuildPack):
    name = Unicode('Dockerfile')
    def detect(self, workdir):
        return os.path.exists(os.path.join(workdir, 'Dockerfile'))

    def build(self, workdir, ref, output_image_spec):
        client = docker.APIClient(base_url='unix://var/run/docker.sock', version='auto')
        for progress in client.build(
                path=workdir,
                tag=output_image_spec,
                decode=True
        ):
            if 'stream' in progress:
                self.log.info(progress['stream'].rstrip(), extra=dict(phase='building'))


class S2IBuildPack(BuildPack):
    # Simple subclasses of S2IBuildPack must set build_image,
    # either via config or during `detect()`
    build_image = Unicode('')
    
    def s2i_build(self, workdir, ref, output_image_spec, build_image):
        # Note: Ideally we'd just copy from workdir here, rather than clone and check out again
        # However, setting just --copy and not specifying a ref seems to check out master for
        # some reason. Investigate deeper FIXME
        cmd = [
            's2i',
            'build',
            '--exclude', '""',
            '--ref', ref,
            '.',
            build_image,
            output_image_spec,
        ]
        env = os.environ.copy()
        # add bundled s2i to *end* of PATH,
        # in case user doesn't have s2i
        env['PATH'] = os.pathsep.join([env.get('PATH') or os.defpath, here])
        try:
            for line in execute_cmd(cmd, cwd=workdir, env=env):
                self.log.info(line, extra=dict(phase='building', builder=self.name))
        except subprocess.CalledProcessError:
            self.log.error('Failed to build image!', extra=dict(phase='failed'))
            sys.exit(1)
    
    def build(self, workdir, ref, output_image_spec):
        return self.s2i_build(workdir, ref, output_image_spec, self.build_image)


class CondaBuildPack(S2IBuildPack):
    """Build Pack for installing from a conda environment.yml using S2I"""

    name = Unicode('conda')
    build_image = Unicode('jupyterhub/singleuser-builder-conda:v0.1.5', config=True)

    def detect(self, workdir):
        return os.path.exists(os.path.join(workdir, 'environment.yml'))


class PythonBuildPack(S2IBuildPack):
    """Build Pack for installing from a pip requirements.txt using S2I"""
    name = Unicode('python-pip')
    runtime_builder_map = Dict({
        'python-2.7': 'jupyterhub/singleuser-builder-venv-2.7:v0.1.5',
        'python-3.5': 'jupyterhub/singleuser-builder-venv-3.5:v0.1.5',
    })

    runtime = Unicode(
        'python-3.5',
        config=True
    )

    def detect(self, workdir):
        if os.path.exists(os.path.join(workdir, 'requirements.txt')):
            try:
                with open(os.path.join(workdir, 'runtime.txt')) as f:
                    self.runtime = f.read().strip()
            except FileNotFoundError:
                pass
            self.build_image = self.runtime_builder_map[self.runtime]
            return True
