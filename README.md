# jupyter-repo2docker


[![Build Status](https://travis-ci.org/jupyter/repo2docker.svg?branch=master)](https://travis-ci.org/jupyter/repo2docker)

**jupyter-repo2docker** is a tool to build, run and push docker images from source code repositories.


## Pre-requisites

1. Docker to build & run the repositories. The [community edition](https://store.docker.com/search?type=edition&offering=community)
   is recommended.
2. Python 3.4+.

## Installation

To install from pypi, the python packaging index:

```bash
pip install jupyter-repo2docker
```

To install from source:

```bash
git clone https://github.com/jupyter/repo2docker.git
cd repo2docker
pip install .
```

## Usage

The core feature of repo2docker is to fetch a repo (from github or locally), build a container
image based on the specifications found in the repo & optionally launch a local Jupyter Notebook
you can use to explore it.

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

## Repository specifications

Repo2Docker looks for various files in the repository being built to figure out how to build it.
It is philosophically similar to [Heroku Build Packs](https://devcenter.heroku.com/articles/buildpacks).

It currently looks for the following files. They are all composable - you can use any number of them
in the same repository (except for Dockerfiles, which take precedence over everything else).

### `requirements.txt`

This specifies a list of python packages that would be installed in a virtualenv (or conda environment).

### `environment.yml`

This is a conda environment specification, that lets you install packages with conda. Note that you must
leave the name of the environment empty for this to work out of the box.

### `apt.txt`

A list of debian packages that should be installed. The base image used is usually the latest released
version of Ubuntu (currently Zesty.)

### `postBuild`

A script that can contain arbitrary commands to be run after the whole repository has been built. If you
want this to be a shell script, make sure the first line is `#!/bin/bash`. This file must have the
executable bit set (`chmod +x postBuild`) to be considered.

### `REQUIRE`

This specifies a list of Julia packages! Currently only version 0.6 of Julia is supported, but more will
be as they are released.

### `Dockerfile`

This will be treated as a regular Dockerfile and a regular Docker build will be performed. The presence
of a Dockerfile will cause all other building behavior to not be triggered.
