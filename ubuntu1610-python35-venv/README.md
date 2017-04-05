
# Ubuntu 16.10 Python3 Virtualenv Jupyter Builder

This is a builder image for use with [s2i](https://github.com/openshift/source-to-image). It
builds a source repository (such as a github repository) into a usable Docker image, without
the user having to use or understand Docker.

It is based off Ubuntu 16.10, and uses [virtualenv](https://pypi.python.org/pypi/virtualenv) to
provide a custom python3.5 environment.

It looks for a `requirements.txt` file in the source repository, and installs it into the virtualenv.
