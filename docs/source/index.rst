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
   faq

.. toctree::
   :maxdepth: 2
   :caption: How-To: User interfaces and environments

   howto/user_interface
   howto/languages
   howto/lab_workspaces

.. toctree::
   :maxdepth: 2
   :caption: How-To: Deployment and administration

   howto/jupyterhub_images
   howto/deploy

.. toctree::
   :maxdepth: 2
   :caption: Complete list of configuration files

   config_files

.. toctree::
   :maxdepth: 2
   :caption: Contribute to repo2docker

   contributing/contributing
   contributing/roadmap
   architecture
   design
   contributing/tasks
   contributing/buildpack

.. toctree::
   :maxdepth: 2
   :caption: Changelog

   changelog
