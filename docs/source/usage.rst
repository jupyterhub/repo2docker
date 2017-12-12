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

.. note::

   See the `Frequently Asked Questions <faq.html>`_ for more info.

Preparing your repository
-------------------------

``repo2docker`` looks for configuration files in the repository being built
to determine how to build it. It is philosophically similar to
`Heroku Build Packs <https://devcenter.heroku.com/articles/buildpacks>`_.
``repo2docker`` will look for files in two places:

* A folder called ``binder`` in the root of the repository.
* The root of the repository. (if a folder called ``binder`` exists in the root
  of the repository, configuration files outside of that folder will be ignored)

.. note::

   In general, ``repo2docker`` uses configuration files that are already part of
   various data science workflows (e.g., ``requirements.txt``), rather than
   creating new custom configuration files.

``repodocker`` configuration files are all composable - you can use any number
of them in the same repository. There are a few notable rules:

* ``Dockerfile``: if a Dockerfile is present in a repository, it will take precedence
  over all other configuration files (which will be ignored).
* ``environment.yml`` with ``requirements.txt``: If both of these files are
  present, then ``environment.yml`` will be used to build the image, **not**
  ``requirements.txt``. If you wish to ``pip install`` packages using an
  ``environment.yml`` file, `you should do so with the
  *pip:* key <https://conda.io/docs/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually>`_.

  .. note::

     For a list of repositories demonstrating various configurations,
     see :ref:`samples`.

.. *** List of all configuratoin files ***
.. include:: config_files.txt

Using ``repo2docker`` with a JupyterHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is possible to use ``repo2docker`` in order to build JupyterHub-ready
Docker images. In order for this to work properly, **the version of the ``jupyterhub``
package in your git repository must match the version in your JupyterHub
deployment**. For example, if your JupyterHub deployment runs ``jupyterhub==0.8``,
you should put the following in ``requirements.txt`` or ``environment.yml``::

  jupyterhub==0.8.*

Running ``repo2docker`` locally
-------------------------------

For information on installing ``repo2docker``, see :ref:`install`.

.. note::

   Docker must be running on your machine in order to build images
   with ``repo2docker``.

Building an image
~~~~~~~~~~~~~~~~~

The simplest invocation of ``repo2docker`` builds a Docker image
from a git repo, then runs a Jupyter server within the image
so you can explore the repository's contents.
You can do this with the following command::

  jupyter-repo2docker https://github.com/jakevdp/PythonDataScienceHandbook

After building (it might take a while!), it should output a message in your terminal::

  Copy/paste this URL into your browser when you connect for the first time,
  to login with a token:
      http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0

If you copy/paste that URL into your browser you will see a Jupyter Notebook with the
contents of the repository you have just built!

Displaying the image Dockerfile
-------------------------------

``repo2docker`` will generate a Dockerfile that composes the created Docker image.
To see the contents of this Dockerfile without building the image use
the ``--debug`` and ``--no-build`` flags like so::

  jupyter-repo2docker --debug --no-build https://github.com/jakevdp/PythonDataScienceHandbook

This will output the contents of the Dockerfile in your console. Note that it
will **not** build the image.

Accessing help from the command line
------------------------------------

For a list of all the build configurations at your disposal, see the
CLI help::

  jupyter-repo2docker -h
