"""Generates a variety of Dockerfiles based on an input matrix
"""
import os
import tempfile
import docker
from .base import BuildPack


class DockerBuildPack(BuildPack):
    """Docker BuildPack"""

    def detect(self):
        """Check if current repo should be built with the Docker BuildPack"""
        return os.path.exists(self.binder_path("Dockerfile"))

    def render(self, build_args=None):
        """
        Render the Dockerfile used by reading it from the source repo

        If an appendix is configured, it will be appended to the Dockerfile
        found in the source repo.
        """
        Dockerfile = self.binder_path("Dockerfile")
        with open(Dockerfile) as f:
            content = f.read()

        if self.appendix:
            content += "\n"
            content += self.appendix

        return content

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

        with tempfile.NamedTemporaryFile(mode="w") as f:
            f.write(self.render())
            f.flush()
            build_kwargs = dict(
                path=os.getcwd(),
                dockerfile=f.name,
                tag=image_spec,
                buildargs=build_args,
                container_limits=limits,
                cache_from=cache_from,
                labels=self.get_labels(),
            )

            build_kwargs.update(extra_build_kwargs)

            for line in client.build(**build_kwargs):
                yield line
