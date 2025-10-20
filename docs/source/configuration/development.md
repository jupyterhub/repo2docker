# Configuration files for software development workflows

(pipfile)=

## `Pipfile` and/or `Pipfile.lock` - Install a Python environment

[pipenv](https://github.com/pypa/pipenv/) allows you to manage a virtual
environment Python dependencies. When using `pipenv`, you end up with
`Pipfile` and `Pipfile.lock` files. The lock file contains explicit details
about the packages that has been installed that met the criteria within the
`Pipfile`.

If both `Pipfile` and `Pipfile.lock` are found by `repo2docker`, the former
will be ignored in favor of the lock file. Also note that these files
distinguish packages and development packages and that `repo2docker` will install
both kinds.

(requirements-txt)=

## `requirements.txt` - Install a Python environment

This specifies a list of Python packages that should be installed in your
environment. Our
[example `requirements.txt` file](https://github.com/binder-examples/requirements/blob/HEAD/requirements.txt)
on GitHub shows a typical requirements file.

(pyproject)=

## `pyproject.toml` - Install Python packages

To install your reprository like a Python package, you may include a
`pyproject.toml` file. `repo2docker`install `pyproject.toml` files by running
`pip install -e .`.

(setup-py)=

## `setup.py` - Install Python packages

```{note}
We recommend to use `pyproject.toml` as it is the recommended way since 2020 when PEPs [621](https://peps.python.org/pep-0621/) and [631](https://peps.python.org/pep-0631/) were accepted.
```

To install your repository like a Python package, you may include a
`setup.py` file. `repo2docker` installs `setup.py` files by running
`pip install -e .`.
