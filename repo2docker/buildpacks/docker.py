"""
Generates a variety of Dockerfiles based on an input matrix
"""
import os
import docker
from .base import BuildPack


class DockerBuildPack(BuildPack):
    name = "Dockerfile"
    dockerfile = "Dockerfile"

    def detect(self):
        return os.path.exists(self.binder_path('Dockerfile'))

    def render(self):
        Dockerfile = self.binder_path('Dockerfile')
        with open(Dockerfile) as f:
            return f.read()

    def build(self, image_spec):
        client = docker.APIClient(version='auto', **docker.utils.kwargs_from_env())
        for line in client.build(
                path=os.getcwd(),
                dockerfile=self.binder_path(self.dockerfile),
                tag=image_spec,
                buildargs={},
                decode=True,
                forcerm=True,
                rm=True
        ):
            yield line
