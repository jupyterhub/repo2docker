Docker - Specifying dependencies
--------------------------------

You can use a Dockerfiles to use a "source" Docker image that has a pre-built
environment. This may be more flexible in running non-standard code.

We recommend sourcing your Dockerfile from one of the Jupyter base images
to ensure that it works with JupyterHub. In this case, we use a stripped-down
image that has minimal dependencies installed.
