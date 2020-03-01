# <a href="https://github.com/jupyter/repo2docker"><img src="https://raw.githubusercontent.com/jupyter/repo2docker/3fa7444fca6ae2b51e590cbc9d83baf92738ca2a/docs/source/_static/images/repo2docker.png" height="48px" /> repo2docker</a>

[![Build Status](https://travis-ci.org/jupyter/repo2docker.svg?branch=master)](https://travis-ci.org/jupyter/repo2docker)
[![Documentation Status](https://readthedocs.org/projects/repo2docker/badge/?version=latest)](http://repo2docker.readthedocs.io/en/latest/?badge=latest)
[![Build Status](https://dev.azure.com/jupyter/repo2docker/_apis/build/status/jupyter.repo2docker?branchName=master)](https://dev.azure.com/jupyter/repo2docker/_build/latest?definitionId=1&branchName=master)
[![Contribute](https://img.shields.io/badge/I_want_to_contribute!-grey?logo=jupyter)](https://repo2docker.readthedocs.io/en/latest/contributing/contributing.html)

`repo2docker` fetches a git repository and builds a container image based on
the configuration files found in the repository.

See the [repo2docker documentation](http://repo2docker.readthedocs.io)
for more information on using repo2docker.

For support questions please search or post to https://discourse.jupyter.org/c/binder.

See the [contributing guide](CONTRIBUTING.md) for information on contributing to
repo2docker.

See [our roadmap](https://repo2docker.readthedocs.io/en/latest/contributing/roadmap.html)
to learn about where the project is heading.

## Using repo2docker
### Prerequisites

1. Docker to build & run the repositories. The [community edition](https://store.docker.com/search?type=edition&offering=community)
   is recommended.
2. Python 3.5+.

Supported on Linux and macOS. [See documentation note about Windows support.](http://repo2docker.readthedocs.io/en/latest/install.html#note-about-windows-support)

### Installation

This a quick guide to installing `repo2docker`, see our documentation for [a full guide](https://repo2docker.readthedocs.io/en/latest/install.html).

We recommend you install the latest and greatest version:
```bash
pip install -U https://github.com/jupyter/repo2docker/archive/master.zip
```
We frequently improve repo2docker and update the version of repo2docker on
mybinder.org a few hours later. This means it is rare that this version
doesn't work.

Roughly every three months we will tag a release which you can install from PyPI:

```bash
pip install -U jupyter-repo2docker
```

To contribute to the documentation or source code you might want to
install and run from a local checkout:

```bash
git clone https://github.com/jupyter/repo2docker.git
cd repo2docker
pip install -e .
```

### Usage

The core feature of repo2docker is to fetch a git repository (from GitHub or locally),
build a container image based on the specifications found in the repository &
optionally launch the container that you can use to explore the repository.

**Note that Docker needs to be running on your machine for this to work.**

Example:

```bash
jupyter-repo2docker https://github.com/norvig/pytudes
```

After building (it might take a while!), it should output in your terminal
something like:

```bash
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0
```

If you copy paste that URL into your browser you will see a Jupyter Notebook
with the contents of the repository you had just built!

For more information on how to use ``repo2docker``, see the
[usage guide](http://repo2docker.readthedocs.io/en/latest/usage.html).


## Repository specifications

Repo2Docker looks for configuration files in the source repository to
determine how the Docker image should be built. For a list of the configuration
files that ``repo2docker`` can use, see the
[complete list of configuration files](https://repo2docker.readthedocs.io/en/latest/config_files.html).

The philosophy of repo2docker is inspired by
[Heroku Build Packs](https://devcenter.heroku.com/articles/buildpacks).
