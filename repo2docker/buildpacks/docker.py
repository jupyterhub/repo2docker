"""Generates a variety of Dockerfiles based on an input matrix
"""
import os
import docker
from .base import BuildPack


class DockerBuildPack(BuildPack):
    """Docker BuildPack"""

    dockerfile = "Dockerfile"

    def detect(self):
        """Check if current repo should be built with the Docker BuildPack"""
        return os.path.exists(self.binder_path("Dockerfile"))

    def render(self):
        """Render the Dockerfile using by reading it from the source repo"""
        Dockerfile = self.binder_path("Dockerfile")
        with open(Dockerfile) as f:
            return f.read()

    def build(
        self,
        client,
        image_spec,
        memory_limit,
        build_args,
        cache_from,
        extra_build_kwargs,
    ):
        """Build a Docker image based on the Dockerfile in the source repo."""
        # If you work on this bit of code check the corresponding code in
        # buildpacks/base.py where it is duplicated
        if not isinstance(memory_limit, int):
            raise ValueError(
                "The memory limit has to be specified as an"
                "integer but is '{}'".format(type(memory_limit))
            )
        limits = {}
        if memory_limit:
            # We want to always disable swap. Docker expects `memswap` to
            # be total allowable memory, *including* swap - while `memory`
            # points to non-swap memory. We set both values to the same so
            # we use no swap.
            limits = {"memory": memory_limit, "memswap": memory_limit}

        build_kwargs = dict(
            path=os.getcwd(),
            dockerfile=self.binder_path(self.dockerfile),
            tag=image_spec,
            buildargs=build_args,
            decode=True,
            forcerm=True,
            rm=True,
            container_limits=limits,
            cache_from=cache_from,
        )

        build_kwargs.update(extra_build_kwargs)

        for line in client.build(**build_kwargs):
            yield line
