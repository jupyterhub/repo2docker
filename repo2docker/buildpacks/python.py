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


class PythonBuildPack(BuildPack):
    name = "python3.5"
    version = "0.1"

    packages = {
        'python3',
        'python3-venv',
        'python3-dev',
    }

    env = [
        ("VENV_PATH", "${APP_BASE}/venv"),
        # Prefix to use for installing kernels and finding jupyter binary
        ("NB_PYTHON_PREFIX", "${VENV_PATH}"),
    ]

    path = [
        "${VENV_PATH}/bin"
    ]

    build_scripts = [
        (
            "root",
            r"""
            mkdir -p ${VENV_PATH} && \
            chown -R ${NB_USER}:${NB_USER} ${VENV_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            python3 -m venv ${VENV_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            pip install --no-cache-dir \
                notebook==5.2.2 \
                ipywidgets==6.0.0 \
                jupyterlab==0.28 && \
            jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
            jupyter serverextension enable --py jupyterlab --sys-prefix
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        # If we have a runtime.txt & that's set to python-2.7,
        # we will *not* install requirements.txt but will find &
        # install a requirements3.txt file if it exists.
        # This way, when using python2 venv, requirements.txt will
        # be installed in the python2 venv, and requirements3.txt
        # will be installed in python3 venv. This is less of a
        # surprise than requiring python2 to be requirements2.txt tho.
        try:
            with open(self.binder_path('runtime.txt')) as f:
                runtime = f.read().strip()
        except FileNotFoundError:
            runtime = 'python-3.5'
        if runtime == 'python-2.7':
            requirements_file = self.binder_path('requirements3.txt')
        else:
            requirements_file = self.binder_path('requirements.txt')
        if os.path.exists(requirements_file):
            return [(
                '${NB_USER}',
                'pip3 install --no-cache-dir -r "{}"'.format(requirements_file)
            )]
        return []

    def detect(self):
        return os.path.exists('requirements.txt') and super().detect()


class Python2BuildPack(BuildPack):
    name = "python2.7"
    version = "0.1"

    packages = {
        'python',
        'python-dev',
        'virtualenv'
    }

    env = [
        ('VENV2_PATH', '${APP_BASE}/venv2')
    ]

    path = [
        "${VENV2_PATH}/bin"
    ]

    build_scripts = [
        (
            "root",
            r"""
            mkdir -p ${VENV2_PATH} && \
            chown -R ${NB_USER}:${NB_USER} ${VENV2_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            virtualenv -p python2 ${VENV2_PATH}
            """
        ),
        (
            "${NB_USER}",
            r"""
            pip2 install --no-cache-dir \
                 ipykernel==4.6.1 && \
            python2 -m ipykernel install --prefix=${NB_PYTHON_PREFIX}
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        return [
            (
                '${NB_USER}',
                'pip2 install --no-cache-dir -r requirements.txt'
            )
        ]

    def detect(self):
        requirements_txt = self.binder_path('requirements.txt')
        runtime_txt = self.binder_path('runtime.txt')
        if os.path.exists(requirements_txt) and os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if runtime == 'python-2.7':
                return True
        return False
