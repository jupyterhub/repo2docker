# Frequently Asked Questions (FAQ)

A collection of frequently asked questions with answers. If you have a question
and have found an answer, send a PR to add it here!

## How should I specify another version of Python?

One can specify a Python version in the ``environment.yml`` file of a repository.

## What versions of Python (or R or Julia...) are supported?

### Python

Repo2docker officially supports the following versions of Python (specified in environment.yml or runtime.txt):

- 3.7 (added in 0.7)
- 3.6 (default)
- 3.5

Additional versions may work, as long as the
[base environment](https://github.com/jupyter/repo2docker/blob/master/repo2docker/buildpacks/conda/environment.yml)
can be installed for your version of Python.
The most likely source of incompatibility is if one of the packages
in the base environment is not packaged for your Python,
either because the version of the package is too new and your chosen Python is too old,
or vice versa.

Additionally, if Python 2.7 is specified,
a separate environment for the kernel will be installed with Python 2.
The notebook server will run in the default Python 3.6 environment.

### Julia

The following versions of Julia are supported (specified in REQUIRE):

- 1.0 (added in 0.7)
- 0.7 (added in 0.7)
- 0.6 (default)

### R

Only R 3.4.4 is currently supported, which is installed via `apt` from the
[ubuntu bionic repository](https://packages.ubuntu.com/bionic/r-base).

## Can I add executable files to the user's PATH?

Yes! With a :ref:`postBuild` file, you can place any files that should be called
from the command line in the folder ``~/.local/``. This folder will be
available in a user's PATH, and can be run from the command line (or as
a subsequent build step.)

## How do I set environment variables?

Use the `-e` or `--env` flag for each variable that you want to define.

For example `jupyter-repo2docker -e VAR1=val1 -e VAR2=val2 ...`

## Can I use repo2docker to bootstrap my own Dockerfile?

No, you can't.

If you pass the `--debug` flag to `repo2docker`, it outputs the intermediate
Dockerfile that is used to build the docker image. While it is tempting to copy
this as a base for your own Dockerfile, that is not supported & in most cases
will not work. The `--debug` output is just our intermediate generated
Dockerfile, and is meant to be built in
[a very specific way](https://github.com/jupyter/repo2docker/blob/master/repo2docker/detectors.py#L381).
Hence the output of `--debug` can not be built with a normal `docker build -t .`
or similar traditional docker command.

Check out the [binder-examples](http://github.com/binder-examples/) GitHub
organization for example repositories you can copy & modify for your own use!

## Can I use repo2docker to edit a local repository within a Docker environment?

Yes: use the `--editable` or `-E` flag (don't confuse it with the `-e`
flag for environment variables), and run repo2docker on a local
repository: `repo2docker -E my-repository/.`.

This builds a Docker container from the files in that repository
(using, for example, a `requirements.txt` file or `Dockerfile`), then
runs that container, while connecting the home directory inside the
container to the local repository outside the container. For example,
in case there is a notebook file (`.ipynb`), this will open in a local
webbrowser, and one can edit it and save it. The resulting notebook is
updated in both the Docker container and the local repository. Once
the container is exited, the changed file will still be in the local
repository.

This allows for easy testing of the container while debugging some
items, as well as using a fully customizable container to edit, for
example, notebooks.

**note**

Editable mode is a convenience option that will mount the repository
to container working directory (usually `/home/$USER`). If you need to
mount to a different location in the container, use the `--volumes`
option instead. Similarly, for a fully customized user Dockerfile,
this option is not guaranteed to work.
