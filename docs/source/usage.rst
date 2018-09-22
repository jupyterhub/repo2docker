.. _usage:

=====================
Using ``repo2docker``
=====================

.. note::

   `Docker <https://docs.docker.com/>`_ **must be running** in
   order to run ``repo2docker``. For more information on installing
   ``repo2docker``, see :ref:`install`.

``repo2docker`` is called with a URL/path to a git repository. It then
performs these steps:

1. Inspects the repository for :ref:`configuration files <config-files>`. These will be used to build
   the environment needed to run the repository.
2. Builds a Docker image with an environment specified in these :ref:`configuration files <config-files>`.
3. Runs a Jupyter server within the image that lets you explore the
   repository interactively (optional)
4. Pushes the images to a Docker registry so that it may be accessed remotely
   (optional)

Calling repo2docker
===================

repo2docker is called with this command::

  jupyter-repo2docker <URL-or-path to repository>

where ``<URL-or-path to repository>`` is a URL or path to the source repository
for which you'd like to build an image.

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


Building a specific branch / commit / tag
=========================================

To build a particular branch and commit, use the argument ``--ref`` and
specify the ``branch-name`` or ``commit-hash``. For example::

  jupyter-repo2docker https://github.com/norvig/pytudes --ref 9ced85dd9a84859d0767369e58f33912a214a3cf

.. tip::
   For reproducible research, we recommend specifying a commit-hash to
   deterministically build a fixed version of a repository. Not specifying a
   commit-hash will result in the latest commit of the repository being built.


Where to put configuration files
================================

``repo2docker`` will look for configuration files in either:

* A folder named ``binder/`` in the root of the repository.
* The root directory of the repository.

If the folder ``binder/`` is located at the top level of the repository,
  **only configuration files in the** ``binder/`` **folder will be considered**.

.. note::

   ``repo2docker`` builds an environment with Python 3.6 by default. If you'd
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

.. _Pytudes: https://github.com/norvig/pytudes
