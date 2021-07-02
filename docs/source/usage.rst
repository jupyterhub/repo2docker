.. _usage:

=====================
Using ``repo2docker``
=====================

.. note::

   `Docker <https://docs.docker.com/>`_ **must be running** in
   order to run ``repo2docker``. For more information on installing
   ``repo2docker``, see :ref:`install`.

``repo2docker`` can build a reproducible computational environment for any repository that
follows :ref:`specification`. repo2docker is called with the URL of a Git repository,
a `DOI  <https://en.wikipedia.org/wiki/Digital_object_identifier>`_ from Zenodo or Figshare,
a `Handle <https://en.wikipedia.org/wiki/Handle_System>`_ or DOI from a Dataverse installation,
a `SWHID`_ of a directory of a revision archived in the
`Software Heritage Archive <https://archive.softwareheritage.org>`_,
or a path to a local directory.

It then performs these steps:

1. Inspects the repository for :ref:`configuration files <config-files>`. These will be used to build
   the environment needed to run the repository.
2. Builds a Docker image with an environment specified in these :ref:`configuration files <config-files>`.
3. Launches the image to let you explore the
   repository interactively via Jupyter notebooks, RStudio, or many other interfaces (optional)
4. Pushes the images to a Docker registry so that it may be accessed remotely
   (optional)

Calling repo2docker
===================

repo2docker is called with this command::

  jupyter-repo2docker <source-repository>

where ``<source-repository>`` is:

  * a URL of a Git repository (``https://github.com/binder-examples/requirements``),
  * a Zenodo DOI (``10.5281/zenodo.1211089``),
  * a SWHID_ (``swh:1:rev:999dd06c7f679a2714dfe5199bdca09522a29649``), or
  * a path to a local directory (``a/local/directory``)

of the source repository you want to build.

For example, the following command will build an image of Peter Norvig's
Pytudes_ repository::

  jupyter-repo2docker https://github.com/norvig/pytudes

Building the image may take a few minutes.

Pytudes_
uses a `requirements.txt file <https://github.com/norvig/pytudes/blob/master/requirements.txt>`_
to specify its Python environment. Because of this, ``repo2docker`` will use
``pip`` to install dependencies listed in this ``requirement.txt`` file, and
these will be present in the generated Docker image. To learn more about
configuration files in ``repo2docker`` visit :ref:`config-files`.

When the image is built, a message will be output to your terminal::

  Copy/paste this URL into your browser when you connect for the first time,
  to login with a token:
      http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0

Pasting the URL into your browser will open Jupyter Notebook with the
dependencies and contents of the source repository in the built image.


Building a specific branch, commit or tag
=========================================

To build a particular branch and commit, use the argument ``--ref`` and
specify the ``branch-name`` or ``commit-hash``. For example::

  jupyter-repo2docker --ref 9ced85dd9a84859d0767369e58f33912a214a3cf https://github.com/norvig/pytudes

.. tip::
   For reproducible builds, we recommend specifying a commit-hash to
   deterministically build a fixed version of a repository. Not specifying a
   commit-hash will result in the latest commit of the repository being built.


.. _usage-config-file-location:

Where to put configuration files
================================

``repo2docker`` will look for configuration files in:

* A folder named ``binder/`` in the root of the repository.
* A folder named ``.binder/`` in the root of the repository.
* The root directory of the repository.

Having both ``binder/`` and ``.binder/`` folders is not allowed.
If one of these folders exists, only configuration files in that folder are considered, configuration in the root directory will be ignored.

Check the complete list of :ref:`configuration files <config-files>` supported
by ``repo2docker`` to see how to configure the build process.

.. note::

   ``repo2docker`` builds an environment with Python 3.7 by default. If you'd
   like a different version, you can specify this in your
   :ref:`configuration files <config-files>`.


Debugging repo2docker with ``--debug`` and ``--no-build``
=========================================================

To debug the docker image being built, pass the ``--debug`` parameter:

  .. code-block:: bash

     jupyter-repo2docker --debug https://github.com/norvig/pytudes

This will print the generated ``Dockerfile``, build it, and run it.

To see the generated ``Dockerfile`` without actually building it,
pass ``--no-build`` to the commandline. This ``Dockerfile`` output
is for **debugging purposes** of ``repo2docker`` only - it can not
be used by docker directly.

  .. code-block:: bash

     jupyter-repo2docker --no-build --debug https://github.com/norvig/pytudes


Command line API
================

.. autoprogram:: repo2docker.__main__:argparser
  :prog: jupyter-repo2docker


.. _Pytudes: https://github.com/norvig/pytudes
.. _SWHID: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html
