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

        pyproject_file = self.binder_path("pyproject.toml")
        with open(pyproject_file, "rb") as _pyproject_file:
            pyproject_toml = tomllib.load(_pyproject_file)

        if "project" in pyproject_toml:
            if "requires-python" in pyproject_toml["project"]:
                raw_version = pyproject_toml["project"]["requires-python"]

                match = VERSION_PAT.match(raw_version)
                if match:
                    return match.group()

        return ""

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
        # install pipenv to install dependencies within Pipfile.lock or Pipfile
        if V(self.python_version) < V("3.6"):
            # last pipenv version to support 2.7, 3.5
            pipenv_version = "2021.5.29"
        else:
            pipenv_version = "2022.1.8"
        scripts.append(
            (
                "${NB_USER}",
                f"${{KERNEL_PYTHON_PREFIX}}/bin/pip install --no-cache-dir pipenv=={pipenv_version}",
            )
        )
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
                """(cd  && \\
                    PATH="${{KERNEL_PYTHON_PREFIX}}/bin:$PATH" \\
                        pip install --no-cache-dir --editable {working_directory}
                )""".format(
                    working_directory=working_directory,
                ),
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
