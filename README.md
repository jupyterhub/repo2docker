# jupyter-repo2docker


[![Build Status](https://travis-ci.org/jupyter/repo2docker.svg?branch=master)](https://travis-ci.org/jupyter/repo2docker)
[![Documentation Status](https://readthedocs.org/projects/repo2docker/badge/?version=latest)](http://repo2docker.readthedocs.io/en/latest/?badge=latest)

**jupyter-repo2docker** takes as input a repository source, such as a GitHub repo. It then builds, runs, and/or pushes Docker images built from
that source.

See the [repo2docker documentation](http://repo2docker.readthedocs.io)
for more information.

## Pre-requisites

1. Docker to build & run the repositories. The [community edition](https://store.docker.com/search?type=edition&offering=community)
   is recommended.
2. Python 3.4+.

## Installation

To install from pypi, the python packaging index:

```bash
pip install jupyter-repo2docker
```

To install from source and start contributing:

```bash
git clone https://github.com/jupyter/repo2docker.git
cd repo2docker
pip install -e .
```

## Usage

The core feature of repo2docker is to fetch a repo (from github or locally), build a container
image based on the specifications found in the repo & optionally launch a local Jupyter Notebook
you can use to explore it.

**Note that Docker needs to be running on your machine for this to work.**

Example:

```bash
jupyter-repo2docker https://github.com/jakevdp/PythonDataScienceHandbook
```

After building (it might take a while!), it should output in your terminal something like:


```
    Copy/paste this URL into your browser when you connect for the first time,
    to login with a token:
        http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0
```

If you copy paste that URL into your browser you will see a Jupyter Notebook with the
contents of the repository you had just built!

For more information on how to use ``repo2docker``, see the
[usage guide](http://repo2docker.readthedocs.io/en/latest/usage.html).

## Repository specifications

Repo2Docker looks for configuration files in the source repository to
determine how the Docker image should be built.
It is philosophically similar to [Heroku Build Packs](https://devcenter.heroku.com/articles/buildpacks).

For a list of the configuration files that ``repo2docker`` can use,
see the [usage guide](http://repo2docker.readthedocs.io/en/latest/usage.html).
