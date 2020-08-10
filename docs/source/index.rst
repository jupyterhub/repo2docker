jupyter-repo2docker
===================

``jupyter-repo2docker`` is a tool to **build, run, and push Docker
images from source code repositories**.

``repo2docker`` fetches a repository
(from GitHub, GitLab, Zenodo, Figshare, Dataverse installations, a Git repository or a local directory)
and builds a container image in which the code can be executed.
The image build process is based on the configuration files found in the repository.

``repo2docker`` can be
used to explore a repository locally by building and executing the
constructed image of the repository, or as a means of building images that
are pushed to a Docker registry.

``repo2docker`` is the tool used by `BinderHub <https://binderhub.readthedocs.io>`_
to build images on demand.

Please report `Bugs <https://github.com/jupyterhub/repo2docker/issues>`_,
`ask questions <https://gitter.im/jupyterhub/binder>`_ or
`contribute to the project <https://github.com/jupyterhub/repo2docker/blob/master/CONTRIBUTING.md>`_.

.. toctree::
   :maxdepth: 2
   :caption: Getting started with repo2docker

   getting-started/index
   howto/index
   configuration/index

.. toctree::
   :maxdepth: 2
   :caption: Contribute to repo2docker

   contributing/index

.. toctree::
   :maxdepth: 2
   :caption: Changelog

   changelog
