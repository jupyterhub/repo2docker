jupyter-repo2docker
-------------------

**jupyter-repo2docker** is a command line tool that builds a docker
image from a git repository. It can also push the image to a docker registry.

Installation
============

To install from pypi, the python packaging index::

    python3 -m pip install jupyter-repo2docker

To install from source::


    git clone https://github.com/jupyterhub/jupyter-repo2docker.git
    cd jupyter-repo2docker

    python3 -m pip install .

Usage
=====

To access help for the application::

    jupyter-repo2docker -h

Technical Overview for Contributors
===================================

**jupyter-repo2docker** uses one of 
([Source to Image](https://github.com/openshift/source-to-image) or Docker)
for building the Docker image.

The ``repo2docker`` directory contains the application that detects which build
method to use, and how to invoke that build method.

The ``s2i-builders`` directory contains builder images which can be used to
provide custom ``conda`` and ``venv`` environments suitable for running
**JupyterHub**.

## Documentation

See the `repo2docker documentation <repo2docker.readthedocs.com>`_ for more
information.
