jupyter-repo2docker
===================

**jupyter-repo2docker** is a tool to deterministically build, run, and
push Docker images from source code repositories. It supports a number of
build file types that install various aspects of a computational environment.
For a list of supported build file types, see the list below, as well as
the :ref:`sample_build_files`.

Installation
------------

You can install ``repo2docker`` with ``pip``::

  pip install jupyter-repo2docker

Usage
-----

Call repo2docker with following command::

  jupyter-repo2docker <path-or-url-to-git-repo>

See the :doc:`api` for more detail on invoking this command.

Site Contents
-------------
.. toctree::
   :maxdepth: 2

   api
   samples
