"""Generates Dockerfiles based on an input matrix based on Python."""
import os

from ..conda import CondaBuildPack


class PythonBuildPack(CondaBuildPack):
    """Setup Python for use with a repository."""

    @property
    def python_version(self):
        if hasattr(self, '_python_version'):
            return self._python_version

        try:
            with open(self.binder_path('runtime.txt')) as f:
                runtime = f.read().strip()
        except FileNotFoundError:
            runtime = ''

        if not runtime.startswith('python-'):
            # not a Python runtime (e.g. R, which subclasses this)
            # use the default Python
            self._python_version = self.major_pythons['3']
            return self._python_version

        py_version_info = runtime.split('-', 1)[1].split('.')
        py_version = ''
        if len(py_version_info) == 1:
            py_version = self.major_pythons[py_version_info[0]]
        else:
            # get major.minor
            py_version = '.'.join(py_version_info[:2])
        self._python_version = py_version
        return self._python_version

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this repository.
        """
        # If we have a runtime.txt & that's set to python-2.7,
        # requirements.txt will be installed in the *kernel* env
        # and requirements3.txt (if it exists)
        # will be installed in the python 3 notebook server env.
        assemble_scripts = super().get_assemble_scripts()
        setup_py = 'setup.py'
        # KERNEL_PYTHON_PREFIX is the env with the kernel,
        # whether it's distinct from the notebook or the same.
        pip = '${KERNEL_PYTHON_PREFIX}/bin/pip'
        if self.py2:
            # using python 2 kernel,
            # requirements3.txt allows installation in the notebook server env
            nb_requirements_file = self.binder_path('requirements3.txt')
            if os.path.exists(nb_requirements_file):
                assemble_scripts.append((
                    '${NB_USER}',
                    # want the $NB_PYHTON_PREFIX environment variable, not for
                    # Python's string formatting to try and replace this
                    '${{NB_PYTHON_PREFIX}}/bin/pip install --no-cache-dir -r "{}"'.format(nb_requirements_file)
                ))

        # install requirements.txt in the kernel env
        requirements_file = self.binder_path('requirements.txt')
        if os.path.exists(requirements_file):
            assemble_scripts.append((
                '${NB_USER}',
                'pip install "pip<19" && ' + \
                '{} install --no-cache-dir -r "{}"'.format(pip, requirements_file)
            ))

        # setup.py exists *and* binder dir is not used
        if not os.path.exists('binder') and os.path.exists(setup_py):
            assemble_scripts.append((
                '${NB_USER}',
                '{} install --no-cache-dir .'.format(pip)
            ))
        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Python buildpack.
        """
        requirements_txt = self.binder_path('requirements.txt')
        runtime_txt = self.binder_path('runtime.txt')
        setup_py = 'setup.py'

        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if runtime.startswith("python-"):
                return True
            else:
                return False
        if not os.path.exists('binder') and os.path.exists(setup_py):
            return True
        return os.path.exists(requirements_txt)
