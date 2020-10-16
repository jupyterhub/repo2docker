"""Buildpack for git repos with poetry.lock or pyproject.toml

`poetry` will be used to install the dependencies conda will provide the base
Python environment, same as the Python or Conda build packs.
"""

import os

from poetry.core.semver import parse_constraint
import toml

from ..conda import CondaBuildPack

#  Minimum version of python for use with Poetry
COMPATIBLE_PYTHON2_VERSIONS = parse_constraint(">=2.7")

#  Min and max compatible versions of python3. N.B. the maximum constraint will
#  have to be manually bumped
COMPATIBLE_PYTHON3_VERSIONS = parse_constraint(">=3.5, <3.10")


class PoetryBuildPack(CondaBuildPack):
    """Setup Python with poetry for use with a repository."""

    @property
    def python_version(self):
        """
        Detect the Python version declared in a `poetry.lock`, `pyproject.toml'.
        Will return 'x.y' if version is found (e.g '3.6'), or a Falsy empty
        string `''` if not found.
        """

        if hasattr(self, "_python_version"):
            return self._python_version

        requested_version = "*"

        pyproject = self.binder_path("pyproject.toml")
        if os.path.exists(pyproject):
            with open(pyproject) as f:
                pyproject_info = toml.load(f)
                specified_version = (
                    pyproject_info.get("tool", {})
                    .get("poetry", {})
                    .get("dependencies", {})
                    .get("python", None)
                )

                if not specified_version is None:
                    requested_version = specified_version

        lockfile = self.binder_path("poetry.lock")
        if os.path.exists(lockfile):
            with open(lockfile) as f:
                lock_info = toml.load(f)
                specified_version = lock_info.get("metadata", {}).get(
                    "python-versions", None
                )

                if not specified_version is None:
                    requested_version = specified_version

        requested_constraint = parse_constraint(requested_version)

        version_range = parse_constraint("*")

        if requested_constraint.allows(parse_constraint("2")):
            version_range = version_range.intersect(COMPATIBLE_PYTHON2_VERSIONS)

        if requested_constraint.allows(parse_constraint("3")):
            #  If the given constraint allows for python 3, then this will
            #  overwrite the range provided by python 2
            version_range = version_range.intersect(COMPATIBLE_PYTHON3_VERSIONS)

        if requested_constraint.allows_any(version_range):
            #  If the requested constraint is in the version range, then the
            #  intersection is non-zero and should be valid, so we narrow the
            #  constraint here
            requested_constraint = version_range.intersect(requested_constraint)
        else:
            #  If the requested constraint not in the version range then most
            #  likely the requested constraint is outside of the the
            #  COMPATIBLE_PYTHON3_VERSIONS, this should only happen if a newer
            #  versions of python is explicitly required, we trust this request
            requested_constraint = requested_constraint.min

        self._python_version = str(requested_constraint.min)

        return self._python_version

    def get_preassemble_script_files(self):
        """Return files needed for preassembly"""
        files = super().get_preassemble_script_files()
        for name in ("requirements3.txt", "pyproject.toml", "poetry.lock"):
            path = self.binder_path(name)
            if os.path.exists(path):
                files[path] = path
        return files

    def get_preassemble_scripts(self):
        """scripts to run prior to staging the repo contents"""
        scripts = super().get_preassemble_scripts()
        # install poetry to install dependencies within poetry.lock or
        # pyproject.toml
        scripts.append(
            ("${NB_USER}", "${KERNEL_PYTHON_PREFIX}/bin/pip install poetry==1.1.3")
        )
        return scripts

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this repository."""
        # If we have either poetry.lock, pyproject.toml, or runtime.txt declare
        # the use of Python 2, Python 2.7 will be made available in the *kernel*
        # environment. The notebook servers environment on the other hand
        # requires Python 3 but may require something additional installed in it
        # still such as `nbgitpuller`. For this purpose, a "requirements3.txt"
        # file will be used to install dependencies for the notebook servers
        # environment, if Python 2 had been specified for the kernel
        # environment.
        assemble_scripts = super().get_assemble_scripts()

        if self.py2:
            # using Python 2 as a kernel, but Python 3 for the notebook server

            # requirements3.txt allows for packages to be installed to the
            # notebook servers Python environment
            nb_requirements_file = self.binder_path("requirements3.txt")
            if os.path.exists(nb_requirements_file):
                assemble_scripts.append(
                    (
                        "${NB_USER}",
                        '${{NB_PYTHON_PREFIX}}/bin/pip install --no-cache-dir -r "{}"'.format(
                            nb_requirements_file
                        ),
                    )
                )

        # pyproject.toml and poetry.lock files can have relative path references
        # so we should be careful about the working directory during the install
        #     [tool.poetry.dependencies]
        #     python = "^3.8"
        #     extra-data = {path = "sampleproject"}
        working_directory = self.binder_dir or "."

        # NOTES:
        # - poetry either uses a configuration file or environment variables for
        #   configuration settings, here we use the inline
        #   `POETRY_VIRTUALENVS_CREATE=false` to tell poetry to not create
        #   another virtual environment during the install and to just install
        #   into the system python environment
        assemble_scripts.append(
            (
                "${NB_USER}",
                """(cd {working_directory} && \\
                    PATH="${{KERNEL_PYTHON_PREFIX}}/bin:$PATH" \\
                        POETRY_VIRTUALENVS_CREATE=false poetry install \\
                )""".format(
                    working_directory=working_directory,
                ),
            )
        )

        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Poetry buildpack."""
        # first make sure python is not explicitly unwanted
        runtime_txt = self.binder_path("runtime.txt")
        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if not runtime.startswith("python-"):
                return False

        pyproject = self.binder_path("pyproject.toml")
        poetry_lock = self.binder_path("poetry.lock")

        is_poetry = False
        if os.path.exists(pyproject):
            with open(pyproject) as f:
                pyproject_info = toml.load(f)
                backend = pyproject_info.get("build-system", {}).get(
                    "build-backend", ""
                )
                is_poetry = backend == "poetry.masonry.api"

        return is_poetry or os.path.exists(poetry_lock)
