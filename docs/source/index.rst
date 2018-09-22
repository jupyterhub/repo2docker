jupyter-repo2docker
===================

``jupyter-repo2docker`` is a tool to **build, run, and push Docker
images from source code repositories** that run via a Jupyter server.

``repo2docker`` fetches a repository
(e.g., from GitHub or other locations) and builds a container image
based on the configuration files found in the repository. It can be
used to explore a repository locally by building and executing the
constructed image of the repository, or as a means of building images that
are pushed to a Docker registry.

Please report `Bugs <https://github.com/jupyter/repo2docker/issues>`_,
`ask questions <https://gitter.im/jupyterhub/binder>`_ or
`contribute to the project <https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md>`_.

.. toctree::
   :maxdepth: 2
   :caption: Getting started with repo2docker

   install
   usage

.. toctree::
   :maxdepth: 1
   :caption: How-to...

   howto/user_interface
   howto/languages
   howto/jupyterhub_images

.. toctree::
   :maxdepth: 2
   :caption: Complete list of configuration files

   config_files

.. toctree::
   :maxdepth: 1
   :caption: Advanced and developer information

   faq
   deploy
   design
   architecture
   dev_newbuildpack
