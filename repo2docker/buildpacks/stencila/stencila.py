"""
Buildpack for stencila editor for DAR document archives
"""

import os
import shutil

from ..conda import CondaBuildPack


class StencilaBuildPack(CondaBuildPack):
    """Stencila buildpack

    - installs stencila in /opt/stencila
    - installs nbserverproxy
    - registers nbserverproxy extension for stencila
    """

    @property
    def runtime(self):
        """
        Return contents of runtime.txt if it exists, '' otherwise
        """
        if not hasattr(self, "_runtime"):
            runtime_path = self.binder_path("runtime.txt")
            try:
                with open(runtime_path) as f:
                    self._runtime = f.read().strip()
            except FileNotFoundError:
                self._runtime = ""

        return self._runtime

    def detect(self):
        """
        Check if current repo should be built with the stencila

        Currently only checks for 'stencila' in runtime.txt
        """
        self.manifest_dir = ""
        for root, dirs, files in os.walk("."):
            for f in files:
                if f == "manifest.xml":
                    self.manifest_dir = os.path.dirname(root)
                    return True
        return self.runtime.startswith("stencila")

    def get_build_env(self):
        """
        Return build environment variables to be set.

        Sets STENCILA_DIR
        """
        return super().get_build_env() + [
            # This is the path where stencila is installed
            ("STENCILA_DIR", "/opt/stencila")
        ]

    def get_env(self):
        """
        Return environment variables to be set.

        Sets STENCILA_ARCHIVE_DIR
        """
        return super().get_env() + [
            ("STENCILA_ARCHIVE_DIR", "${HOME}/" + self.manifest_dir)
        ]

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.
        """
        return super().get_build_script_files()

    def get_build_scripts(self):
        """
        Install commands for stencila
        """
        return super().get_build_scripts() + [
            (
                "root",
                r"""
                mkdir -p ${STENCILA_DIR} && \
                chown -R ${NB_USER}:${NB_USER} ${STENCILA_DIR}
                """,
            ),
            (
                "${NB_USER}",
                # install nbserverproxy
                r"""
                pip install --no-cache https://github.com/minrk/nbserverproxy/archive/del-starting.tar.gz
                """,
            ),
            (
                "${NB_USER}",
                # install stencila
                r"""
                cd ${STENCILA_DIR} && \
                npm install 'https://github.com/minrk/jupyter-dar#2c1c54089502ebdb6ad44d15d63259108a0ab141'
                """,
            ),
            (
                "${NB_USER}",
                # install stencila
                r"""
                conda install -yq numpy matplotlib && \
                conda clean -tipsy
                """,
            ),
        ]

    def get_assemble_scripts(self):
        """Return assembly scripts to run after staging repo contents"""
        assemble_scripts = super().get_assemble_scripts()
        assemble_scripts.extend(
            [
                (
                    "${NB_USER}",
                    r"""
                    pip install --no-cache https://github.com/minrk/jupyter-dar/archive/master.tar.gz && \
                    jupyter serverextension enable --sys-prefix --py nbstencilaproxy && \
                    jupyter nbextension install    --sys-prefix --py nbstencilaproxy && \
                    jupyter nbextension enable     --sys-prefix --py nbstencilaproxy
                    """,
                )
            ]
        )
        return assemble_scripts
