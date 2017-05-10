import os
import subprocess

import docker

from traitlets import Unicode, Dict
from traitlets.config import LoggingConfigurable


class BuildPack(LoggingConfigurable):
    def detect(self, workdir):
        """
        Return True if app in workdir can be built with this buildpack
        """
        pass

    def build(self, workdir, output_image_spec):
        """
        Run a command that will take workdir and produce an image ready to be pushed
        """
        pass



class DockerBuildPack(BuildPack):
    def detect(self, workdir):
        return os.path.exists(os.path.join(workdir, 'Dockerfile'))

    def build(self, workdir, output_image_spec):
        client = docker.APIClient(base_url='unix://var/run/docker.sock', version='auto')
        for progress in client.build(
                path=workdir,
                tag=output_image_spec,
                decode=True
        ):
            # FIXME: Properly stream back useful information only
            pass


class PythonBuildPack(BuildPack):
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
            return True

    def build(self, workdir, output_image_spec):
        cmd = [
            's2i',
            'build',
            workdir,
            self.runtime_builder_map[self.runtime],
            output_image_spec
        ]
        subprocess.check_call(cmd)
