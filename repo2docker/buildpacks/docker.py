"""Generates a variety of Dockerfiles based on an input matrix
"""
import os
import docker
from .base import BuildPack


class DockerBuildPack(BuildPack):
    """Docker BuildPack"""
    dockerfile = "Dockerfile"

    @property
    def dockerfile_path(self):
        return self.binder_path(self.dockerfile)

    def detect(self):
        """Check if current repo should be built with the Docker BuildPack"""
        return os.path.exists(self.dockerfile_path)

    def render(self):
        """Render the Dockerfile using by reading it from the source repo"""
        with open(self.dockerfile_path) as f:
            return '{}\n{}'.format(f.read(), self.appendix)

    def build(self, image_spec, memory_limit, build_args):
        """Build a Docker image based on the Dockerfile in the source repo."""
        # first extend dockerfile with appendix
        dockerfile = self.render()  # add the appendix
        with open(self.dockerfile_path, 'w') as f:
            f.write(dockerfile)

        limits = {
            # Always disable memory swap for building, since mostly
            # nothing good can come of that.
            'memswap': -1
        }
        if memory_limit:
            limits['memory'] = memory_limit
        client = docker.APIClient(version='auto', **docker.utils.kwargs_from_env())
        for line in client.build(
                path=os.getcwd(),
                dockerfile=self.dockerfile_path,
                tag=image_spec,
                buildargs=build_args,
                decode=True,
                forcerm=True,
                rm=True,
                container_limits=limits
        ):
            yield line
