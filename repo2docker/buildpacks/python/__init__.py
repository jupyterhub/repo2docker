"""
Generates a variety of Dockerfiles based on an input matrix
"""
import os
from ..base import BaseImage


class PythonBuildPack(BaseImage):
    def get_packages(self):
        return super().get_packages().union({
            'python3',
            'python3-venv',
            'python3-dev',
        })

    def get_env(self):
        return super().get_env() + [
            ("VENV_PATH", "${APP_BASE}/venv"),
            # Prefix to use for installing kernels and finding jupyter binary
            ("NB_PYTHON_PREFIX", "${VENV_PATH}"),
        ]

    def get_path(self):
        return super().get_path() + [
            "${VENV_PATH}/bin"
        ]


    def get_build_script_files(self):
        files = {
            'python/requirements.frozen.txt': '/tmp/requirements.frozen.txt',
        }
        files.update(super().get_build_script_files())
        return files

    def get_build_scripts(self):
        return super().get_build_scripts() + [
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
                pip install --no-cache-dir -r /tmp/requirements.frozen.txt && \
                jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
                jupyter serverextension enable --py jupyterlab --sys-prefix && \
                jupyter serverextension enable nteract_on_jupyter --sys-prefix
                """
            )
        ]

    def get_assemble_scripts(self):
        # If we have a runtime.txt & that's set to python-2.7,
        # we will *not* install requirements.txt but will find &
        # install a requirements3.txt file if it exists.
        # This way, when using python2 venv, requirements.txt will
        # be installed in the python2 venv, and requirements3.txt
        # will be installed in python3 venv. This is less of a
        # surprise than requiring python2 to be requirements2.txt tho.
        assemble_scripts = super().get_assemble_scripts()
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
            assemble_scripts.append((
                '${NB_USER}',
                'pip3 install --no-cache-dir -r "{}"'.format(requirements_file)
            ))
        return assemble_scripts

    def detect(self):
        return os.path.exists('requirements.txt') and super().detect()


class Python2BuildPack(PythonBuildPack):
    def get_packages(self):
        return super().get_packages().union({
            'python',
            'python-dev',
            'virtualenv'
        })


    def get_env(self):
        return super().get_env() + [
            ('VENV2_PATH', '${APP_BASE}/venv2')
        ]

    def get_path(self):
        return super().get_path() + [
            "${VENV2_PATH}/bin"
        ]

    def get_build_script_files(self):
        files = {
            'python/requirements2.frozen.txt': '/tmp/requirements2.frozen.txt',
        }
        files.update(super().get_build_script_files())
        return files

    def get_build_scripts(self):
        return super().get_build_scripts() + [
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
                pip2 install --no-cache-dir -r /tmp/requirements2.frozen.txt && \
                python2 -m ipykernel install --prefix=${NB_PYTHON_PREFIX}
                """
            )
        ]

    def get_assemble_scripts(self):
        return super().get_assemble_scripts() + [
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
