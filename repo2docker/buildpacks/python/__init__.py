"""Generates Dockerfiles based on an input matrix based on Python."""
import os

from ..conda import CondaBuildPack
from ...utils import is_local_pip_requirement, open_guess_encoding


class PythonBuildPack(CondaBuildPack):
    """Setup Python for use with a repository."""

    @property
    def python_version(self):
        if hasattr(self, "_python_version"):
            return self._python_version

        try:
            with open(self.binder_path("runtime.txt")) as f:
                runtime = f.read().strip()
        except FileNotFoundError:
            runtime = ""

        if not runtime.startswith("python-"):
            # not a Python runtime (e.g. R, which subclasses this)
            # use the default Python
            self._python_version = self.major_pythons["3"]
            return self._python_version

        py_version_info = runtime.split("-", 1)[1].split(".")
        py_version = ""
        if len(py_version_info) == 1:
            py_version = self.major_pythons[py_version_info[0]]
        else:
            # get major.minor
            py_version = ".".join(py_version_info[:2])
        self._python_version = py_version
        return self._python_version

    def _get_pip_scripts(self):
        """Get pip install scripts

        added to preassemble unless local references are found,
        in which case this happens in assemble.
        """
        # KERNEL_PYTHON_PREFIX is the env with the kernel,
        # whether it's distinct from the notebook or the same.
        pip = "${KERNEL_PYTHON_PREFIX}/bin/pip"
        scripts = []
        if self.py2:
            # using python 2 kernel,
            # requirements3.txt allows installation in the notebook server env
            nb_requirements_file = self.binder_path("requirements3.txt")
            if os.path.exists(nb_requirements_file):
                scripts.append(
                    (
                        "${NB_USER}",
                        # want the $NB_PYHTON_PREFIX environment variable, not for
                        # Python's string formatting to try and replace this
                        '${{NB_PYTHON_PREFIX}}/bin/pip install --no-cache-dir -r "{}"'.format(
                            nb_requirements_file
                        ),
                    )
                )

        # install requirements.txt in the kernel env
        requirements_file = self.binder_path("requirements.txt")
        if os.path.exists(requirements_file):
            scripts.append(
                (
                    "${NB_USER}",
                    '{} install --no-cache-dir -r "{}"'.format(pip, requirements_file),
                )
            )
        return scripts

    @property
    def _should_preassemble_pip(self):
        """Peek in requirements.txt to determine if we can assemble from only env files

        If there are any local references, e.g. `-e .`,
        stage the whole repo prior to installation.
        """
        if not os.path.exists("binder") and os.path.exists("setup.py"):
            # can't install from subset if we're using setup.py
            return False
        for name in ("requirements.txt", "requirements3.txt"):
            requirements_txt = self.binder_path(name)
            if not os.path.exists(requirements_txt):
                continue
            with open_guess_encoding(requirements_txt) as f:
                for line in f:
                    if is_local_pip_requirement(line):
                        return False

        # didn't find any local references,
        # allow assembly from subset
        return True

    def get_preassemble_script_files(self):
        assemble_files = super().get_preassemble_script_files()
        for name in ("requirements.txt", "requirements3.txt"):
            requirements_txt = self.binder_path(name)
            if os.path.exists(requirements_txt):
                assemble_files[requirements_txt] = requirements_txt
        return assemble_files

    def get_preassemble_scripts(self):
        """Return scripts to run before adding the full repository"""
        scripts = super().get_preassemble_scripts()
        if self._should_preassemble_pip:
            scripts.extend(self._get_pip_scripts())
        return scripts

    def get_assemble_scripts(self):
        """Return series of build steps that require the full repository"""
        # If we have a runtime.txt & that's set to python-2.7,
        # requirements.txt will be installed in the *kernel* env
        # and requirements3.txt (if it exists)
        # will be installed in the python 3 notebook server env.
        assemble_scripts = super().get_assemble_scripts()
        setup_py = "setup.py"
        # KERNEL_PYTHON_PREFIX is the env with the kernel,
        # whether it's distinct from the notebook or the same.
        pip = "${KERNEL_PYTHON_PREFIX}/bin/pip"
        if not self._should_preassemble_pip:
            assemble_scripts.extend(self._get_pip_scripts())

        # setup.py exists *and* binder dir is not used
        if not self.binder_dir and os.path.exists(setup_py):
            assemble_scripts.append(
                ("${NB_USER}", "{} install --no-cache-dir .".format(pip))
            )
        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Python buildpack."""
        requirements_txt = self.binder_path("requirements.txt")
        runtime_txt = self.binder_path("runtime.txt")
        setup_py = "setup.py"

        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if runtime.startswith("python-"):
                return True
            else:
                return False
        if not self.binder_dir and os.path.exists(setup_py):
            return True
        return os.path.exists(requirements_txt)
