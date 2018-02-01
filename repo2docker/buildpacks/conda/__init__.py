"""
Buildpack for conda environments
"""
import glob
import os
import re

from ruamel.yaml import YAML
from traitlets import default, Unicode

from ..base import BuildPack

# pattern for parsing conda dependency line
PYTHON_REGEX = re.compile(r'python\s*=+\s*([\d\.]*)')
# current directory
HERE = os.path.dirname(os.path.abspath(__file__))


class CondaBuildPack(BuildPack):
    name = "conda"
    version = "0.1"
    def get_env(self):
        return [
            ('CONDA_DIR', '${APP_BASE}/conda'),
            ('NB_PYTHON_PREFIX', '${CONDA_DIR}'),
        ]

    def get_path(self):
        return ['${CONDA_DIR}/bin']

    def get_build_scripts(self):
        return [
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
        '3': '3.6',
    }

    def get_build_script_files(self):
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
        return files

    @property
    def python_version(self):
        """
        Detect the Python version for a given environment.yml

        Will return 'x.y' if found, or Falsy '' if not.
        """
        if not hasattr(self, '_python_version'):
            environment_yml = self.binder_path('environment.yml')
            if not os.path.exists(environment_yml):
                self._python_version = ''
            with open(environment_yml) as f:
                env = YAML().load(f)
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
                    self._python_version = '.'.join(py_version[:2])

            self._python_version = ''
        return self._python_version

    @property
    def py2(self):
        """Am I building a Python 2 kernel environment?"""
        return self.python_version and self.python_version.split('.')[0] == '2'

    #@default('assemble_scripts')
    def setup_assembly(self):
        assembly_scripts = []
        environment_yml = self.binder_path('environment.yml')
        env_name = 'kernel' if self.py2 else 'root'
        if os.path.exists(environment_yml):
            assembly_scripts.append((
                '${NB_USER}',
                r"""
                conda env update -v -n {} -f "{}" && \
                conda clean -tipsy
                """.format(env_name, environment_yml)
            ))
        return assembly_scripts


    def detect(self):
        return os.path.exists(self.binder_path('environment.yml')) and super().detect()
