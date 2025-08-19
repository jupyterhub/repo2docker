"""Buildpack for Git repositories with pyproject.toml

Support to pyproject.toml was added to pip v10.0,
see https://pip.pypa.io/en/latest/reference/build-system/pyproject-toml/.
"""

import os
import re
import tomllib
from functools import lru_cache

from ..conda import CondaBuildPack

VERSION_PAT = re.compile(r"\d+(\.\d+)*")


class PyprojectBuildPack(CondaBuildPack):
    """Setup Python with pyproject.toml for use with a repository."""

    @property
    def python_version(self):
        """
        Detect the Python version declared in a `pyproject.toml`.
        Will return 'x.y' if version is found (e.g '3.6'),
        or a Falsy empty string '' if not found.
        """

        if hasattr(self, "_python_version"):
            return self._python_version

        try:
            with open(self.binder_path("runtime.txt")) as f:
                runtime = f.read().strip()
        except FileNotFoundError:
            runtime = ""

        if runtime.startswith("python-"):
            runtime_python_version = runtime.split("-", 1)[1]
        else:
            # not a Python runtime (e.g. R, which subclasses this)
            # use the default Python
            runtime_python_version = self.major_pythons["3"]
            self.log.warning(
                f"Python version unspecified in runtime.txt, using current default Python version {runtime_python_version}. This will change in the future."
            )

        runtime_python_version_info = runtime_python_version.split(".")
        if len(runtime_python_version_info) == 1:
            runtime_python_version = self.major_pythons[runtime_python_version_info[0]]
            runtime_python_version_info = runtime_python_version.split(".")

        pyproject_file = self.binder_path("pyproject.toml")
        with open(pyproject_file, "rb") as _pyproject_file:
            pyproject_toml = tomllib.load(_pyproject_file)

        if "project" in pyproject_toml:
            if "requires-python" in pyproject_toml["project"]:
                # This is the minumum version!
                raw_pyproject_minimum_version = pyproject_toml["project"][
                    "requires-python"
                ]

                match = VERSION_PAT.match(raw_pyproject_minimum_version)
                if match:
                    pyproject_minimum_version = match.group()
                    pyproject_minimum_version_info = pyproject_minimum_version.split(
                        "."
                    )

                    if (
                        runtime_python_version_info[0]
                        < pyproject_minimum_version_info[0]
                    ) or (
                        runtime_python_version_info[1]
                        < pyproject_minimum_version_info[1]
                    ):
                        raise RuntimeError(
                            "runtime.txt version not supported by pyproject.toml."
                        )

        self._python_version = runtime_python_version
        return self._python_version

    @lru_cache
    def get_preassemble_script_files(self):
        """Return files needed for preassembly"""
        files = super().get_preassemble_script_files()
        path = self.binder_path("pyproject.toml")
        if os.path.exists(path):
            files[path] = path
        return files

    @lru_cache
    def get_preassemble_scripts(self):
        """scripts to run prior to staging the repo contents"""
        scripts = super().get_preassemble_scripts()
        return scripts

    @lru_cache
    def get_assemble_scripts(self):
        """Return series of build-steps specific to this repository."""
        # If we have pyproject.toml declare the
        # use of Python 2, Python 2.7 will be made available in the *kernel*
        # environment. The notebook servers environment on the other hand
        # requires Python 3 but may require something additional installed in it
        # still such as `nbgitpuller`. For this purpose, a "requirements3.txt"
        # file will be used to install dependencies for the notebook servers
        # environment, if Python 2 had been specified for the kernel
        # environment.
        assemble_scripts = super().get_assemble_scripts()

        if self.separate_kernel_env:
            # using legacy Python (e.g. 2.7) as a kernel

            # requirements3.txt allows for packages to be installed to the
            # notebook servers Python environment
            nb_requirements_file = self.binder_path("requirements3.txt")
            if os.path.exists(nb_requirements_file):
                assemble_scripts.append(
                    (
                        "${NB_USER}",
                        f'${{NB_PYTHON_PREFIX}}/bin/pip install --no-cache-dir -r "{nb_requirements_file}"',
                    )
                )

        assemble_scripts.append(
            (
                "${NB_USER}",
                "${KERNEL_PYTHON_PREFIX}/bin/pip install --no-cache-dir --editable .",
            )
        )

        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the pyproject.toml buildpack."""
        # first make sure python is not explicitly unwanted
        runtime_txt = self.binder_path("runtime.txt")
        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if not runtime.startswith("python-"):
                return False

        pyproject_file = self.binder_path("pyproject.toml")

        return os.path.exists(pyproject_file)
