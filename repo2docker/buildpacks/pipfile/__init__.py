"""Buildpack for git repos with Pipfile.lock or Pipfile

`pipenv` will be used to install the dependencies
conda will provide the base Python environment,
same as the Python or Conda build packs.
"""

import json
import os
import re

import toml

from ..conda import CondaBuildPack

VERSION_PAT = re.compile(r"\d+(\.\d+)*")


class PipfileBuildPack(CondaBuildPack):
    """Setup Python with pipfile for use with a repository."""

    @property
    def python_version(self):
        """
        Detect the Python version declared in a `Pipfile.lock`, `Pipfile`, or
        `runtime.txt`. Will return 'x.y' if version is found (e.g '3.6'), or a
        Falsy empty string '' if not found.
        """

        if hasattr(self, "_python_version"):
            return self._python_version

        files_to_search_in_order = [
            self.binder_path("Pipfile.lock"),
            self.binder_path("Pipfile"),
        ]

        lockfile = self.binder_path("Pipfile.lock")
        requires_sources = []
        if os.path.exists(lockfile):
            with open(lockfile) as f:
                lock_info = json.load(f)
                requires_sources.append(lock_info.get("_meta", {}).get("requires", {}))

        pipfile = self.binder_path("Pipfile")
        if os.path.exists(pipfile):
            with open(pipfile) as f:
                pipfile_info = toml.load(f)
            requires_sources.append(pipfile_info.get("requires", {}))

        py_version = None
        for requires in requires_sources:
            for key in ("python_full_version", "python_version"):
                version_str = requires.get(key, None)
                if version_str:
                    match = VERSION_PAT.match(version_str)
                    if match:
                        py_version = match.group()
                if py_version:
                    break
            if py_version:
                break

        # extract major.minor
        if py_version:
            if len(py_version.split(".")) == 1:
                self._python_version = self.major_pythons.get(py_version[0])
            else:
                # return major.minor
                self._python_version = ".".join(py_version.split(".")[:2])
            return self._python_version
        else:
            # use the default Python
            self._python_version = self.major_pythons["3"]
            return self._python_version

    def get_preassemble_script_files(self):
        """Return files needed for preassembly"""
        files = super().get_preassemble_script_files()
        for name in ("requirements3.txt", "Pipfile", "Pipfile.lock"):
            path = self.binder_path(name)
            if os.path.exists(path):
                files[path] = path
        return files

    def get_preassemble_scripts(self):
        """scripts to run prior to staging the repo contents"""
        scripts = super().get_preassemble_scripts()
        # install pipenv to install dependencies within Pipfile.lock or Pipfile
        scripts.append(
            ("${NB_USER}", "${KERNEL_PYTHON_PREFIX}/bin/pip install pipenv==2018.11.26")
        )
        return scripts

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this repository."""
        # If we have either Pipfile.lock, Pipfile, or runtime.txt declare the
        # use of Python 2, Python 2.7 will be made available in the *kernel*
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

        pipfile = self.binder_path("Pipfile")
        pipfile_lock = self.binder_path("Pipfile.lock")

        # A Pipfile(.lock) can contain relative references, so we need to be
        # mindful about where we invoke pipenv as that will dictate where .`
        # referes to.
        #     [packages]
        #     my_package_example = {path=".", editable=true}
        working_directory = self.binder_dir or "."

        # NOTES:
        # - Without prioritizing the PATH to KERNEL_PYTHON_PREFIX over
        #   NB_SERVER_PYTHON_PREFIX, 'pipenv' draws the wrong conclusion about
        #   what Python environment is the '--system' environment.
        # - The --system flag allows us to avoid wrapping ourself in yet
        #   another virtual environment that we also then need to enter.
        #   This flag is only available within the `install` subcommand of
        #   `pipenv`.
        # - The `--skip-lock` will not run the `lock` subcommand again as
        #   part of the `install` command. This allows a preexisting .lock
        #   file to remain intact and be used directly. This allows us to
        #   prioritize usage of .lock files that makes sense for
        #   reproducibility.
        # - The `--ignore-pipfile` requires a .lock file to be around as if
        #   there isn't, no other option remain.
        # - The '\\' will is within a Python """ """ string render to a '\'. A
        #   Dockerfile where this later is read within, will thanks to the '\'
        #   let the RUN command continue on the next line. So it is only added
        #   to avoid forcing us to write it all on a single line.
        assemble_scripts.append(
            (
                "${NB_USER}",
                """(cd {working_directory} && \\
                    PATH="${{KERNEL_PYTHON_PREFIX}}/bin:$PATH" \\
                        pipenv install {install_option} --system --dev \\
                )""".format(
                    working_directory=working_directory,
                    install_option="--ignore-pipfile"
                    if os.path.exists(pipfile_lock)
                    else "--skip-lock",
                ),
            )
        )

        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Pipfile buildpack."""
        # first make sure python is not explicitly unwanted
        runtime_txt = self.binder_path("runtime.txt")
        if os.path.exists(runtime_txt):
            with open(runtime_txt) as f:
                runtime = f.read().strip()
            if not runtime.startswith("python-"):
                return False

        pipfile = self.binder_path("Pipfile")
        pipfile_lock = self.binder_path("Pipfile.lock")

        return os.path.exists(pipfile) or os.path.exists(pipfile_lock)
