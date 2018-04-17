.. _usage:

Using ``repo2docker``
=====================

The core functionality of repo2docker is to fetch a repo (e.g., from GitHub or
other locations) and build a container image based on the specifications found in the
repo. Optionally, it can launch a local Jupyter Notebook which you can use to explore it.

This section describes the general ways in which you can use
``repo2docker``, including:

.. contents::
   :depth: 1
   :local:


See the `Frequently Asked Questions <faq.html>`_ for additional information.

Preparing your repository
-------------------------

``repo2docker`` looks for configuration files in the repository being built
to determine how to build it. It is philosophically similar to
`Heroku Build Packs <https://devcenter.heroku.com/articles/buildpacks>`_.

Locating and composing configuration files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``repo2docker`` will look for configuration files **located** in two places:

* A folder called ``binder`` in the root of the repository.
* The root of the repository. (If a folder called ``binder`` exists in the root
  of the repository, configuration files outside of that folder will be ignored.)

.. note::

   In general, ``repo2docker`` uses configuration files that are already part of
   various data science workflows (e.g., ``requirements.txt``), rather than
   creating new custom configuration files.

``repo2docker`` configuration files are all **composable** - you can use any number
of them in the same repository. 

There are a few notable rules for composition precedence and build priority:

* ``Dockerfile``: If a Dockerfile is present in a repository, it will take precedence
  over all other configuration files (which will be ignored).
* ``environment.yml`` with ``requirements.txt``: If both of these files are
  present, then ``environment.yml`` will be used to build the image, **not**
  ``requirements.txt``. If you wish to ``pip install`` packages using an
  ``environment.yml`` file, you should do so with the
  ``pip:`` key as described in the `conda documentation`_.

  .. note::

     For a list of repositories demonstrating various configurations,
     see :ref:`samples`.

.. *** List of all configuration files ***
.. include:: config_files.txt

Preparing a repo to build JupyterHub-ready images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to use ``repo2docker`` to build JupyterHub-ready
Docker images. For this to work properly, the version of the ``jupyterhub``
package in your git repository must match the version in your JupyterHub
deployment. For example, if your JupyterHub deployment runs ``jupyterhub==0.8``,
you should put the following in ``requirements.txt`` or ``environment.yml``::

  jupyterhub==0.8.*

Running ``repo2docker`` locally
-------------------------------

For information on installing ``repo2docker``, see :ref:`install`.

.. note::

   Docker must be running on your machine in order to build images
   with ``repo2docker``.

The simplest invocation of ``repo2docker`` performs two steps:

1. builds a Docker image from a git repo
2. runs a Jupyter server within the image

This two step process enables you to build an image and run it so you can
explore the repository's contents.

The **command** used is::

  jupyter-repo2docker <URL-or-path to repo>

where ``<URL-or-path to repo>`` provides a URL or path to the source repository.

For example, use the following to build an image and launch a Jupyter Notebook
server::

  jupyter-repo2docker https://github.com/jakevdp/PythonDataScienceHandbook

When the example completes building (which may take a few minutes), a message will
be output to your terminal::

  Copy/paste this URL into your browser when you connect for the first time,
  to login with a token:
      http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0

If you copy/paste that URL into your browser you will see a Jupyter Notebook with the
contents of the source repository which you have just built.

Using the ``--debug`` and ``--no-build`` parameters
---------------------------------------------------

If you want to debug and understand the details of the docker image being built,
you can pass the ``debug`` parameter to the commandline:

  .. code-block:: bash

     jupyter-repo2docker --debug https://github.com/jakevdp/PythonDataScienceHandbook

This will print the generated ``Dockerfile``, build it, and run it.

To see the generated ``Dockerfile`` without actually building it,
pass ``--no-build`` to the commandline. This ``Dockerfile`` output
is for **debugging purposes** of ``repo2docker`` only - it can not
be used by docker directly.

  .. code-block:: bash

     jupyter-repo2docker --no-build --debug https://github.com/jakevdp/PythonDataScienceHandbook

Setting environment variables
-----------------------------

If you want to define environment variables, you can pass the ``--env`` or ``-e`` parameter to the commandline:

  .. code-block:: bash

     jupyter-repo2docker -e VAR1=val1 -e VAR2=val2 ...

Accessing help from the command line
------------------------------------

For a list of all the build configurations at your disposal, see the
CLI help::

  jupyter-repo2docker -h

.. _conda documentation: https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually
