"""
DEPRECATED - Dependencies of REQUIRE have been removed
"""

import os

from ..python import PythonBuildPack


class JuliaRequireBuildPack(PythonBuildPack):
    """
    Julia build pack which uses conda and REQUIRE.

    Now just an informative error message.
    """

    def build(self, *args, **kwargs):
        raise ValueError(
            "Julia REQUIRE no longer supported due to removed infrastructure. Use Project.toml."
        )

    def detect(self):
        """
        Check if current repo exects tp be built with the Julia Legacy Build pack

        This no longer works, but try to raise an informative error.
        """
        return os.path.exists(self.binder_path("REQUIRE")) and not (
            os.path.exists(self.binder_path("Project.toml"))
            or os.path.exists(self.binder_path("JuliaProject.toml"))
        )
