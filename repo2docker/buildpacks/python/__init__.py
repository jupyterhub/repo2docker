"""Generates Dockerfiles based on an input matrix based on Python."""

import os
import re
from functools import lru_cache

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from ...utils import is_local_pip_requirement, open_guess_encoding
from ..conda import CondaBuildPack


class PythonBuildPack(CondaBuildPack):
    """Setup Python for use with a repository."""

    @property
    def python_version(self):
        if hasattr(self, "_python_version"):
            return self._python_version

        name, version, _ = self.runtime

        if name != "python" or not version:
            # Either not specified, or not a Python runtime (e.g. R, which subclasses this)
            # use the default Python
            self._python_version = self.major_pythons["3"]
            self.log.warning(
                f"Python version unspecified, using current default Python version {self._python_version}. This will change in the future."
            )
            return self._python_version

        py_version_info = version.split(".")
        py_version = ""
        if len(py_version_info) == 1:
            py_version = self.major_pythons[py_version_info[0]]
        else:
            # get major.minor
            py_version = ".".join(py_version_info[:2])
        self._python_version = py_version

        pyproject_toml = "pyproject.toml"
        if not self.binder_dir and os.path.exists(pyproject_toml):
            with open(pyproject_toml, "rb") as _pyproject_file:
                pyproject = tomllib.load(_pyproject_file)

            if "project" in pyproject:
                if "requires-python" in pyproject["project"]:
                    # This is the minumum version!
                    raw_pyproject_minimum_version = pyproject["project"][
                        "requires-python"
                    ]

                    match = re.compile(r"\d+(\.\d+)*").match(
                        raw_pyproject_minimum_version
                    )
                    if match:
                        pyproject_minimum_version = match.group()
                        pyproject_minimum_version_info = (
                            pyproject_minimum_version.split(".")
                        )

                        if (py_version_info[0] < pyproject_minimum_version_info[0]) or (
                            py_version_info[1] < pyproject_minimum_version_info[1]
                        ):
                            raise RuntimeError(
                                "runtime.txt version not supported by pyproject.toml."
                            )

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
        if self.separate_kernel_env:
            # using legacy Python kernel
            # requirements3.txt allows installation in the notebook server env
            nb_requirements_file = self.binder_path("requirements3.txt")
            if os.path.exists(nb_requirements_file):
                scripts.append(
                    (
                        "${NB_USER}",
                        # want the $NB_PYHTON_PREFIX environment variable, not for
                        # Python's string formatting to try and replace this
                        f'${{NB_PYTHON_PREFIX}}/bin/pip install --no-cache-dir -r "{nb_requirements_file}"',
                    )
                )

        # install requirements.txt in the kernel env
        requirements_file = self.binder_path("requirements.txt")
        if os.path.exists(requirements_file):
            scripts.append(
                (
                    "${NB_USER}",
                    f'{pip} install --no-cache-dir -r "{requirements_file}"',
                )
            )
        return scripts

    @property
    def _should_preassemble_pip(self):
        """Peek in requirements.txt to determine if we can assemble from only env files

        If there are any local references, e.g. `-e .`,
        stage the whole repo prior to installation.
        """
        # can't install from subset
        for _configuration_file in ("pyproject.toml", "setup.py"):
            if not os.path.exists("binder") and os.path.exists(_configuration_file):
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

    @lru_cache
    def get_preassemble_script_files(self):
        assemble_files = super().get_preassemble_script_files()
        for name in ("requirements.txt", "requirements3.txt"):
            requirements_txt = self.binder_path(name)
            if os.path.exists(requirements_txt):
                assemble_files[requirements_txt] = requirements_txt
        return assemble_files

    @lru_cache
    def get_preassemble_scripts(self):
        """Return scripts to run before adding the full repository"""
        scripts = super().get_preassemble_scripts()
        if self._should_preassemble_pip:
            scripts.extend(self._get_pip_scripts())
        return scripts

    @lru_cache
    def get_assemble_scripts(self):
        """Return series of build steps that require the full repository"""
        # If we have a runtime.txt & that's set to python-2.7,
        # requirements.txt will be installed in the *kernel* env
        # and requirements3.txt (if it exists)
        # will be installed in the python 3 notebook server env.
        assemble_scripts = super().get_assemble_scripts()
        # KERNEL_PYTHON_PREFIX is the env with the kernel,
        # whether it's distinct from the notebook or the same.
        pip = "${KERNEL_PYTHON_PREFIX}/bin/pip"
        if not self._should_preassemble_pip:
            assemble_scripts.extend(self._get_pip_scripts())

        for _configuration_file in ("pyproject.toml", "setup.py"):
            if not self.binder_dir and os.path.exists(_configuration_file):
                assemble_scripts.append(
                    ("${NB_USER}", f"{pip} install --no-cache-dir .")
                )
                break

        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Python buildpack."""
        requirements_txt = self.binder_path("requirements.txt")
        pyproject_toml = "pyproject.toml"
        setup_py = "setup.py"

        name = self.runtime[0]
        if name:
            return name == "python"
        if not self.binder_dir and os.path.exists(pyproject_toml):
            with open(pyproject_toml, "rb") as _pyproject_file:
                pyproject = tomllib.load(_pyproject_file)

            if (
                ("project" in pyproject)
                and ("build-system" in pyproject)
                and ("requires" in pyproject["build-system"])
            ):
                return True

        if not self.binder_dir and os.path.exists(setup_py):
            return True
        return os.path.exists(requirements_txt)
