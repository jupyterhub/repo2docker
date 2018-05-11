"""
Buildpack for stencila editor for DAR document archives
"""

import os

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
        self.manifest_dir = ''
        for root, dirs, files in os.walk('.'):
            print(root, dirs, files)
            for f in files:
                if f == 'manifest.xml':
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
            ("STENCILA_DIR", "/opt/stencila"),
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

        Includes files required for running stencila

        This currently adds a frozen set of Python requirements to the dict
        of files.

        """
        files = super().get_build_script_files()
        files[
            "stencila/jupyter_notebook_config.py"
        ] = "/etc/jupyter/jupyter_notebook_config.py"
        files[
            "stencila/stencila-ext.json"
        ] = "/etc/jupyter/jupyter_notebook_config.d/stencila-ext.json"
        return files

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
                pip install https://github.com/minrk/nbserverproxy/archive/del-starting.tar.gz
                """,
            ),
            (
                "${NB_USER}",
                # install stencila
                r"""
                cd ${STENCILA_DIR} && \
                npm install https://github.com/minrk/jupyter-dar
                """,
            ),
        ]

    def get_assemble_scripts(self):
        """Return assembly scripts to run after staging repo contents"""
        assemble_scripts = super().get_assemble_scripts()
        return assemble_scripts
