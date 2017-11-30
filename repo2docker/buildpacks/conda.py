"""
Generates a variety of Dockerfiles based on an input matrix
"""
import textwrap
from traitlets.config import LoggingConfigurable
from traitlets import Unicode, Set, List, Dict, Tuple, default
from textwrap import dedent
import jinja2
import tarfile
import io
import os
import stat
import re
import docker
from .base import BuildPack


class CondaBuildPack(BuildPack):
    name = "conda"
    version = "0.1"
    env = [
        ('CONDA_DIR', '${APP_BASE}/conda'),
        ('NB_PYTHON_PREFIX', '${CONDA_DIR}')
    ]

    path = ['${CONDA_DIR}/bin']

    build_script_files = {
        'conda/install-miniconda.bash': '/tmp/install-miniconda.bash',
        'conda/environment.yml': '/tmp/environment.yml'
    }

    build_scripts = [
        (
            "root",
            r"""
            bash /tmp/install-miniconda.bash && \
            rm /tmp/install-miniconda.bash /tmp/environment.yml
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        assembly_scripts = []
        environment_yml = self.binder_path('environment.yml')
        if os.path.exists(environment_yml):
            assembly_scripts.append((
                '${NB_USER}',
                r"""
                conda env update -v -n root -f "{}" && \
                conda clean -tipsy
                """.format(environment_yml)
            ))
        return assembly_scripts

    def detect(self):
        return os.path.exists(self.binder_path('environment.yml')) and super().detect()
