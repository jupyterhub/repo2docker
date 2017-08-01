Docker - Specifying dependencies
--------------------------------

You can specify dependencies with Dockerfiles, which may be more flexible
in running non-standard code. We recommend sourcing your Dockerfile from
one of the Jupyter base images. In this case, we use a stripped-down image
that has minimal dependencies installed.
