"""Generates Dockerfiles from the legacy Binder Dockerfiles
based on `andrewosh/binder-base`.

The Dockerfile is amended to add the contents of the repository
to the image and install a supported version of the notebook
and IPython kernel.

Note: This buildpack has been deprecated.
"""
import logging


class LegacyBinderDockerBuildPack:
    """Legacy build pack for compatibility to first version of Binder.

    This buildpack has been deprecated.
    """

    def detect(self):
        """Check if current repo should be built with the Legacy BuildPack."""
        log = logging.getLogger("repo2docker")
        try:
            with open("Dockerfile", "r") as f:
                for line in f:
                    if line.startswith("FROM"):
                        if "andrewosh/binder-base" in line.split("#")[0].lower():
                            log.error(
                                "The legacy buildpack was removed in January 2020."
                            )
                            log.error(
                                "Please see https://repo2docker.readthedocs.io/en/"
                                "latest/configuration/index.html for alternative ways "
                                "of configuring your repository."
                            )
                            raise RuntimeError("The legacy buildpack has been removed.")
                        else:
                            return False
        except FileNotFoundError:
            pass

        return False
