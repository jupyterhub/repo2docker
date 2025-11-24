"""Generates Dockerfiles based on an input matrix based on Python."""

import os
import re
from functools import lru_cache

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from packaging.specifiers import InvalidSpecifier, SpecifierSet
from packaging.version import Version

from ...utils import is_local_pip_requirement, open_guess_encoding
from ..conda import CondaBuildPack


class PythonBuildPack(CondaBuildPack):
    """Setup Python for use with a repository."""

    @property
    def python_version(self):
        if hasattr(self, "_python_version"):
            return self._python_version

        name, version, _ = self.runtime

        if name is not None and name != "python":
            # Runtime specified, but not Python (e.g. R, which subclasses this)
            # use the default Python
            self._python_version = self.major_pythons["3"]
            self._python_version_source = "default"
            self.log.warning(
                f"Python version unspecified, using current default Python version {self._python_version}. This will change in the future."
            )
            return self._python_version

        if name is None or version is None:
            self._python_version = self.major_pythons["3"]
            self._python_version_source = "default"
            self.log.warning(
                f"Python version unspecified, using current default Python version {self._python_version}. This will change in the future."
            )
        else:
            if len(Version(version).release) <= 1:
                self._python_version = self.major_pythons[version]
                self._python_version_source = "default"
            else:
                self._python_version = version
                self._python_version_source = "runtime"

        runtime_version = Version(self._python_version)

        pyproject_toml = "pyproject.toml"
        if not self.binder_dir and os.path.exists(pyproject_toml):
            with open(pyproject_toml, "rb") as _pyproject_file:
                pyproject = tomllib.load(_pyproject_file)

            if "project" in pyproject and "requires-python" in pyproject["project"]:
                # This is the minumum version!
                # https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#python-requires
                pyproject_python_specifier = SpecifierSet(
                    pyproject["project"]["requires-python"]
                )

                if runtime_version not in pyproject_python_specifier:
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
        if self._is_python_package():
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
    def _is_python_package(self):
        if self.binder_dir:
            return False
        if os.path.exists("setup.py"):
            return True
        if os.path.exists("pyproject.toml"):
            with open("pyproject_toml", "rb") as _pyproject_file:
                pyproject = tomllib.load(_pyproject_file)

            if ("project" in pyproject) and ("build-system" in pyproject):
                return True
        return False

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

        if self._is_python_package():
            assemble_scripts.append(("${NB_USER}", f"{pip} install --no-cache-dir ."))

        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Python buildpack."""
        requirements_txt = self.binder_path("requirements.txt")

        name = self.runtime[0]
        if name:
            return name == "python"

        if self._is_python_package():
            return True

        return os.path.exists(requirements_txt)
