"""BuildPack for conda environments"""
import os
import re
from collections import Mapping

from ruamel.yaml import YAML

from ..base import BaseImage

# pattern for parsing conda dependency line
PYTHON_REGEX = re.compile(r'python\s*=+\s*([\d\.]*)')
# current directory
HERE = os.path.dirname(os.path.abspath(__file__))


class CondaBuildPack(BaseImage):
    """A conda BuildPack.

    Uses miniconda since it is more lightweight than Anaconda.

    """
    def get_build_env(self):
        """Return environment variables to be set.

        We set `CONDA_DIR` to the conda install directory and
        the `NB_PYTHON_PREFIX` to the location of the jupyter binary.

        """
        env = super().get_build_env() + [
            ('CONDA_DIR', '${APP_BASE}/conda'),
            ('NB_PYTHON_PREFIX', '${CONDA_DIR}'),
        ]
        if self.py2:
            env.append(('KERNEL_PYTHON_PREFIX', '${CONDA_DIR}/envs/kernel'))
        else:
            env.append(('KERNEL_PYTHON_PREFIX', '${NB_PYTHON_PREFIX}'))
        return env

    def get_path(self):
        """Return paths (including conda environment path) to be added to
        the PATH environment variable.

        """
        path = super().get_path()
        if self.py2:
            path.insert(0, '${KERNEL_PYTHON_PREFIX}/bin')
        path.insert(0, '${CONDA_DIR}/bin')
        return path

    def get_build_scripts(self):
        """
        Return series of build-steps common to all Python 3 repositories.

        All scripts here should be independent of contents of the repository.

        This sets up through `install-miniconda.bash` (found in this directory):

        - a directory for the conda environment and its ownership by the
          notebook user
        - a Python 3 interpreter for the conda environment
        - a Python 3 jupyter kernel
        - a frozen base set of requirements, including:
            - support for Jupyter widgets
            - support for JupyterLab
            - support for nteract

        """
        return super().get_build_scripts() + [
            (
                "root",
                r"""
                bash /tmp/install-miniconda.bash && \
                rm /tmp/install-miniconda.bash /tmp/environment.yml
                """
            )
        ]

    major_pythons = {
        '2': '2.7',
        '3': '3.7',
    }

    def get_build_script_files(self):
        """
        Dict of files to be copied to the container image for use in building.

        This is copied before the `build_scripts` & `assemble_scripts` are
        run, so can be executed from either of them.

        It's a dictionary where the key is the source file path in the host
        system, and the value is the destination file path inside the
        container image.

        This currently adds a frozen set of Python requirements to the dict
        of files.

        """
        files = {
            'conda/install-miniconda.bash': '/tmp/install-miniconda.bash',
        }
        py_version = self.python_version
        self.log.info("Building conda environment for python=%s" % py_version)
        # Select the frozen base environment based on Python version.
        # avoids expensive and possibly conflicting upgrades when changing
        # major Python versions during upgrade.
        # If no version is specified or no matching X.Y version is found,
        # the default base environment is used.
        frozen_name = 'environment.frozen.yml'
        if py_version:
            if self.py2:
                # python 2 goes in a different env
                files['conda/environment.py-2.7.frozen.yml'] = '/tmp/kernel-environment.yml'
            else:
                py_frozen_name = \
                    'environment.py-{py}.frozen.yml'.format(py=py_version)
                if os.path.exists(os.path.join(HERE, py_frozen_name)):
                    frozen_name = py_frozen_name
                else:
                    self.log.warning("No frozen env: %s", py_frozen_name)
        files['conda/' + frozen_name] = '/tmp/environment.yml'
        files.update(super().get_build_script_files())
        return files

    @property
    def python_version(self):
        """Detect the Python version for a given `environment.yml`

        Will return 'x.y' if version is found (e.g '3.6'),
        or a Falsy empty string '' if not found.

        """
        environment_yml = self.binder_path('environment.yml')
        if not os.path.exists(environment_yml):
            return ''

        if not hasattr(self, '_python_version'):
            py_version = None
            with open(environment_yml) as f:
                env = YAML().load(f)
                # check if the env file is empty, if so instantiate an empty dictionary.
                if env is None:
                    env = {}
                # check if the env file provided a dick-like thing not a list or other data structure.
                if not isinstance(env, Mapping):
                    raise TypeError("environment.yml should contain a dictionary. Got %r" % type(env))
                for dep in env.get('dependencies', []):
                    if not isinstance(dep, str):
                        continue
                    match = PYTHON_REGEX.match(dep)
                    if not match:
                        continue
                    py_version = match.group(1)
                    break

            # extract major.minor
            if py_version:
                if len(py_version) == 1:
                    self._python_version = self.major_pythons.get(py_version[0])
                else:
                    # return major.minor
                    self._python_version = '.'.join(py_version.split('.')[:2])
            else:
                self._python_version = ''

        return self._python_version

    @property
    def py2(self):
        """Am I building a Python 2 kernel environment?"""
        return self.python_version and self.python_version.split('.')[0] == '2'

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this source repository.
        """
        assembly_scripts = []
        environment_yml = self.binder_path('environment.yml')
        env_name = 'kernel' if self.py2 else 'root'
        if os.path.exists(environment_yml):
            assembly_scripts.append((
                '${NB_USER}',
                r"""
                conda env update -n {0} -f "{1}" && \
                conda clean -tipsy && \
                conda list -n {0}
                """.format(env_name, environment_yml)
            ))
        return super().get_assemble_scripts() + assembly_scripts

    def detect(self):
        """Check if current repo should be built with the Conda BuildPack.
        """
        return os.path.exists(self.binder_path('environment.yml')) and super().detect()
