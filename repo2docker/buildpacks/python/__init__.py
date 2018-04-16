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
            runtime = 'python-' + self.major_pythons['3']
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
        # we will *not* install requirements.txt but will find &
        # install a requirements3.txt file if it exists.
        # This way, when using python2 env, requirements.txt will
        # be installed in the python2 env, and requirements3.txt
        # will be installed in python3 env. This is less of a
        # surprise than requiring python2 to be requirements2.txt tho.
        assemble_scripts = super().get_assemble_scripts()
        setup_py = 'setup.py'
        pip = 'pip'
        if self.py2:
            # using python 2 kernel,
            # requirements3.txt allows installation in the notebook env
            nb_requirements_file = self.binder_path('requirements3.txt')
            if os.path.exists(nb_requirements_file):
                assemble_scripts.append((
                    '${NB_USER}',
                    'pip install --no-cache-dir -r "{}"'.format(nb_requirements_file)
                ))
            # subsequent `pip` calls should run in the kernel env
            pip = '${KERNEL_PYTHON_PREFIX}/bin/pip'

        # install requirements.txt in the kernel env
        requirements_file = self.binder_path('requirements.txt')
        if os.path.exists(requirements_file):
            assemble_scripts.append((
                '${NB_USER}',
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
