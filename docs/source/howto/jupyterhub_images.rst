.. _jupyterhub_images:

=============================
Build JupyterHub-ready images
=============================

JupyterHub_ allows multiple
users to collaborate on a shared Jupyter server. ``repo2docker`` can build
Docker images that can be shared within a JupyterHub deployment.  For example,
`mybinder.org <https://mybinder.org>`_ uses JupyterHub and ``repo2docker``
to allow anyone to build a Docker image of a git repository online and
share an executable version of the repository with a URL to the built image.

To build JupyterHub_-ready Docker images with ``repo2docker``, the
version of your JupyterHub deployment must be included in the
``environment.yml`` or ``requirements.txt`` of the git repositories you
build.

If your instance of JupyterHub uses ``DockerSpawner``, you will need to set its
command to run ``jupyterhub-singleuser`` by adding this line in your
configuration file::

  c.DockerSpawner.cmd = ['jupyterhub-singleuser']

.. _JupyterHub: https://github.com/jupyterhub/jupyterhub
