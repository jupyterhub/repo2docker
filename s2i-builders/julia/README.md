
# JupyterHub singleuser builder

This is a builder image for use with [s2i](https://github.com/openshift/source-to-image). It
builds a source repository (such as a github repository) into a docker image that is suitable
for use with [JupyterHub](http://github.com/jupyterhub/jupyterhub).

It is based off Ubuntu 17.04, and uses [virtualenv](https://pypi.python.org/pypi/virtualenv) to
provide a custom python3.5 environment.

It looks for a `requirements.txt` file in the source repository, and installs it into the virtualenv.
It also installs a number of default notebook related modules in there
