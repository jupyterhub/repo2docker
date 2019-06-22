"""Buildpack for git repos with Pipfile.lock or Pipfile within them. `pipenv`
will be used to install the dependencies but we will manually install declared
Python versions instead of using PyEnv."""

import os
import re

from ..conda import CondaBuildPack


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
            {
                "path": self.binder_path("Pipfile.lock"),
                "pattern": r"\s*\"python_(?:full_)?version\": \"?([0-9a-z\.]*)\"?",  # '            "python_version": "3.6"'
            },
            {
                "path": self.binder_path("Pipfile"),
                "pattern": r"python_(?:full_)?version\s*=+\s*\"?([0-9a-z\.]*)\"?",  # 'python_version = "3.6"'
            },
            {
                "path": self.binder_path("runtime.txt"),
                "pattern": r"\s*python-([0-9a-z\.]*)\s*",  # 'python-3.6'
            },
        ]

        py_version = None
        for file in files_to_search_in_order:
            try:
                with open(file["path"]) as f:
                    for line in f:
                        match = re.match(file["pattern"], line)
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
                self._python_version = ".".join(py_version.split(".")[:2])
            return self._python_version
        else:
            # use the default Python
            self._python_version = self.major_pythons["3"]
            return self._python_version

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this repository.
        """
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
            # using python 2 kernel,
            # requirements3.txt allows installation in the notebook server env
            nb_requirements_file = self.binder_path("requirements3.txt")
            if os.path.exists(nb_requirements_file):
                assemble_scripts.append(
                    (
                        "${NB_USER}",
                        # want the $NB_PYHTON_PREFIX environment variable, not for
                        # Python's string formatting to try and replace this
                        '${{NB_PYTHON_PREFIX}}/bin/pip install --no-cache-dir -r "{}"'.format(
                            nb_requirements_file
                        ),
                    )
                )

        # install Pipfile.lock or fallback to installing Pipfile
        pipenv = "${KERNEL_PYTHON_PREFIX}/bin/pipenv"
        python = "${KERNEL_PYTHON_PREFIX}/bin/python"
        pipfile = self.binder_path("Pipfile")
        pipfile_lock = self.binder_path("Pipfile.lock")
        # let pipenv work relative to the dir that has the Pipfile, it is
        # important as they can contain relative references such as:
        #     my_package = {path=".", editable=true}
        working_directory = self.binder_dir or "."
        assemble_scripts.append(("${NB_USER}", "pip install pipenv"))
        # if Pipfile.lock isn't found, Pipfile is used to create one
        if not os.path.exists(pipfile_lock):
            assemble_scripts.append(
                (
                    "${NB_USER}",
                    "(cd {} && {} lock --python {})".format(
                        working_directory, pipenv, python
                    ),
                )
            )
        # install Pipfile.lock
        assemble_scripts.append(
            (
                "${NB_USER}",
                "(cd {} && {} install --ignore-pipfile --deploy --system --dev --python {})".format(
                    working_directory, pipenv, python
                ),
            )
        )

        return assemble_scripts

    def detect(self):
        """Check if current repo should be built with the Pipfile buildpack.
        """
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
