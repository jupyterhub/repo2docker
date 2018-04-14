"""Generates Dockerfiles based on an input matrix based on Python."""
import os

from ..base import BaseImage


class PythonBuildPack(BaseImage):
    """Setup Python 3 for use with a repository."""
    def get_packages(self):
        """Return a list of the Python 3 core language packages to be installed
           via apt-get for this BuildPack.

           Note: The packages specified here are for the core Python3 language.
           Third party libraries are specified in other configuration files.

        """
        return super().get_packages().union({
            'python3',
            'python3-venv',
            'python3-dev',
        })

    def get_env(self):
        """
        Return environment variables to be set.

        We set `VENV_PATH` to the virtual environment location and
        the `NB_PYTHON_PREFIX` to the location of the jupyter binary.

        """
        return super().get_env() + [
            ("VENV_PATH", "${APP_BASE}/venv"),
            # Prefix to use for installing kernels and finding jupyter binary
            ("NB_PYTHON_PREFIX", "${VENV_PATH}"),
        ]

    def get_path(self):
        """Return paths (including virtual environment path) to be added to
        the PATH environment variable.

        """
        return super().get_path() + [
            "${VENV_PATH}/bin"
        ]

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.

        This currently adds a frozen set of Python 3 requirements to the dict
        of files.

        """
        files = {
            'python/requirements.frozen.txt': '/tmp/requirements.frozen.txt',
        }
        files.update(super().get_build_script_files())
        return files

    def get_build_scripts(self):
        """
        Return series of build-steps common to all Python 3 repositories.

        All scripts here should be independent of contents of the repository.

        This sets up:

        - a directory for the virtual environment and its ownership by the
          notebook user
        - a Python 3 interpreter for the virtual environement
        - a Python 3 jupyter kernel including a base set of requirements
        - support for Jupyter widgets
        - support for JupyterLab
        - support for nteract

        """
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
        """Return series of build-steps specific to this repository.
        """
        # If we have a runtime.txt & that's set to python-2.7,
        # we will *not* install requirements.txt but will find &
        # install a requirements3.txt file if it exists.
        # This way, when using python2 venv, requirements.txt will
        # be installed in the python2 venv, and requirements3.txt
        # will be installed in python3 venv. This is less of a
        # surprise than requiring python2 to be requirements2.txt tho.
        assemble_scripts = super().get_assemble_scripts()
        setup_py = 'setup.py'
        try:
            with open(self.binder_path('runtime.txt')) as f:
                runtime = f.read().strip()
        except FileNotFoundError:
            runtime = 'python-3.5'
        if runtime == 'python-2.7':
            pip = "pip2"
            requirements_file = self.binder_path('requirements3.txt')
        else:
            pip = "pip3"
            requirements_file = self.binder_path('requirements.txt')
        if os.path.exists(requirements_file):
            assemble_scripts.append((
                '${NB_USER}',
                'pip3 install --no-cache-dir -r "{}"'.format(requirements_file)
            ))
        if not os.path.exists('binder') and os.path.exists(setup_py):
            assemble_scripts.append((
                '${NB_USER}',
                '{} install --no-cache-dir .'.format(pip)
            ))
        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Python 3 Build pack.
        """
        requirements_txt = self.binder_path('requirements.txt')
        runtime_txt = self.binder_path('runtime.txt')
        setup_py = 'setup.py'

        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if runtime.startswith("python-3"):
                return True
            else:
                return False
        if not os.path.exists('binder') and os.path.exists(setup_py):
            return True
        return os.path.exists(requirements_txt)


class Python2BuildPack(PythonBuildPack):
    """Setup Python 2 for use with a repository."""
    def get_packages(self):
        """Return a list of the Python 2 core language packages to be installed
           via apt-get for this BuildPack.

           Note: The packages specified here are for the core Python2 language.
           Third party libraries are specified in other configuration files.

        """
        return super().get_packages().union({
            'python',
            'python-dev',
            'virtualenv'
        })

    def get_env(self):
        """
        Return environment variables to be set.

        We set `VENV_PATH` to the virtual environment location containing
        Python 2.

        """
        return super().get_env() + [
            ('VENV2_PATH', '${APP_BASE}/venv2')
        ]

    def get_path(self):
        """Return paths (including virtual environment path) to be added to
        the PATH environment variable.

        """
        return super().get_path() + [
            "${VENV2_PATH}/bin"
        ]

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.

        This currently adds a frozen set of Python 2 requirements to the dict
        of files.

        """
        files = {
            'python/requirements2.frozen.txt': '/tmp/requirements2.frozen.txt',
        }
        files.update(super().get_build_script_files())
        return files

    def get_build_scripts(self):
        """
        Return series of build-steps common to all Python 2 repositories.

        All scripts here should be independent of contents of the repository.

        This sets up:

        - a directory for the virtual environment and its ownership by the
          notebook user
        - a Python 2 interpreter for the virtual environement
        - a Python 2 jupyter kernel

        """
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
        """Return series of build-steps specific to this repository.
        """
        requirements_txt = self.binder_path('requirements.txt')
        assemble_scripts = super().get_assemble_scripts()
        if os.path.exists(requirements_txt):
            assemble_scripts.insert(0, (
                '${NB_USER}',
                'pip2 install --no-cache-dir -r "{}"'.format(requirements_txt)
            ))
        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Python 2 Build pack.
        """
        runtime_txt = self.binder_path('runtime.txt')

        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if runtime == 'python-2.7':
                return True
            elif runtime.startswith('python-2'):
                raise ValueError(
                    "Only python-2.7 or python-3.x is supported in "
                    "runtime.txt, not '{}'".format(runtime_txt))
            else:
                return False
        return False
