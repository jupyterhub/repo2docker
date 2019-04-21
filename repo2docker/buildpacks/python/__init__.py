"""Generates Dockerfiles based on an input matrix based on Python."""
import os
import re

from ..conda import CondaBuildPack

class PythonBuildPack(CondaBuildPack):
    """Setup Python for use with a repository."""

    @property
    def python_version(self):
        """
        Detect the Python version declared in a `Pipfile.lock`, `Pipfile`, or
        `runtime.txt`. Will return 'x.y' if version is found (e.g '3.6'), or a
        Falsy empty string '' if not found.
        """

        if hasattr(self, '_python_version'):
            return self._python_version

        files_to_search_in_order = [
            {
                'path': self.binder_path('Pipfile.lock'),
                'pattern': r'\s*\"python_(?:full_)?version\": \"?([0-9a-z\.]*)\"?', # '            "python_version": "3.6"'
            },
            {
                'path': self.binder_path('Pipfile'),
                'pattern': r'python_(?:full_)?version\s*=+\s*\"?([0-9a-z\.]*)\"?', # 'python_version = "3.6"'
            },
            {
                'path': self.binder_path('runtime.txt'),
                'pattern': r'\s*python-([0-9a-z\.]*)\s*', # 'python-3.6'
            },
        ]

        py_version = None
        for file in files_to_search_in_order:
            try:
                with open(file['path']) as f:
                    for line in f:
                        match = re.match(file['pattern'], line)
                        if not match:
                            continue
                        py_version = match.group(1)
                        break
            except FileNotFoundError:
                pass
            if py_version:
                break

        # extract major.minor
        if py_version:
            if len(py_version) == 1:
                self._python_version = self.major_pythons.get(py_version[0])
            else:
                # return major.minor
                self._python_version = '.'.join(py_version.split('.')[:2])
            return self._python_version
        else:
            # use the default Python
            self._python_version = self.major_pythons['3']
            return self._python_version

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this repository.
        """
        # If we have a runtime.txt & that's set to python-2.7,
        # requirements.txt will be installed in the *kernel* env
        # and requirements3.txt (if it exists)
        # will be installed in the python 3 notebook server env.
        assemble_scripts = super().get_assemble_scripts()

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

        # install Pipfile.lock, Pipfile, or requirements.txt in the kernel env
        pipenv = '${KERNEL_PYTHON_PREFIX}/bin/pipenv'
        pipfile = self.binder_path('Pipfile')
        pipfile_lock = self.binder_path('Pipfile.lock')
        if os.path.exists(pipfile_lock) or os.path.exists(pipfile):
            assemble_scripts.append((
                '${NB_USER}',
                'pip install pipenv'
            ))
            if not os.path.exists(pipfile_lock):
                assemble_scripts.append((
                    '${NB_USER}',
                    '{} lock --python {}'.format(pipenv, '${KERNEL_PYTHON_PREFIX}/bin/python')
                ))
            assemble_scripts.append((
                '${NB_USER}',
                '{} install --ignore-pipfile --deploy --system --dev --python {}'.format(pipenv, '${KERNEL_PYTHON_PREFIX}/bin/python')
            ))
        else:
            # KERNEL_PYTHON_PREFIX is the env with the kernel,
            # whether it's distinct from the notebook or the same.
            pip = '${KERNEL_PYTHON_PREFIX}/bin/pip'
            requirements_file = self.binder_path('requirements.txt')
            setup_py = 'setup.py'
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
        pipfile = self.binder_path('Pipfile')
        pipfile_lock = self.binder_path('Pipfile.lock')
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
        return os.path.exists(pipfile) or os.path.exists(pipfile_lock) or os.path.exists(requirements_txt)
