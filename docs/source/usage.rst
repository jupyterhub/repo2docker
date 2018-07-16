.. _usage:

Using ``repo2docker``
=====================

`Docker <https://docs.docker.com/>`_ **must be running** in
order to run ``repo2docker``. For more information on installing
``repo2docker``, see :ref:`install`.

``repo2docker`` performs two steps:

1. builds a Docker image from a git repo
2. runs a Jupyter server within the image to explore the repo

To ensure you can run the software in your repository, you must

repo2docker is called with this command::

  jupyter-repo2docker <URL-or-path to repo>

where ``<URL-or-path to repo>`` is a URL or path to the source repository.

For example, use the following to build an image of the
`Python Pytudes notebook <https://github.com/norvig/pytudes>`_::

  jupyter-repo2docker https://github.com/norvig/pytudes

To build a particular branch and commit, use the argument ``--ref`` to
specify the ``branch-name`` or ``commit-hash``::

  jupyter-repo2docker https://github.com/norvig/pytudes --ref 9ced85dd9a84859d0767369e58f33912a214a3cf

.. tip::
   For reproducibile research, we recommend specifying a commit-hash to
   deterministcally build a fixed version of a repository. Not specifying a
   commit-hash will result in the latest commit of the repository being built.

Building the image may take a few minutes.

During building, ``repo2docker``
clones the repository to obtain its contents and inspects the repo for
:ref:`configuration files <config-files>`.

By default, ``repo2docker`` will assume you are using
Python 3.6 unless you include the version of Python in your
:ref:`configuration files <config-files>`.  ``repo2docker`` support is best with
Python 2.7, 3.5, and 3.6.  In the case of this repo, a Python version is not
specified in their configuation files and Python 3.6 is installed.

`Python Pytudes Repository <https://github.com/norvig/pytudes>`_
uses a `requirements.txt file <https://github.com/norvig/pytudes/blob/master/requirements.txt>`_
to specify its Python environment. ``repo2docker`` uses ``pip`` to install
dependencies listed in the ``requirement.txt`` in the image. To learn more about
configuration files in ``repo2docker`` visit :ref:`config-files`.

When the image is built, a message will be output to your terminal::

  Copy/paste this URL into your browser when you connect for the first time,
  to login with a token:
      http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0

Pasting the URL into your browser will open Jupyter Notebook with the
dependencies and contents of the source repository in the built image.

Because JupyterLab is a server extension of the classic Jupyter Notebook server,
you can launch JupyterLab by opening Jupyter Notebook and visiting the
```/lab`` to the end of the URL:

.. code-block:: none

   http(s)://<server:port>/<lab-location>/lab

To switch back to the classic notebook, add ``/tree`` to the URL:

.. code-block:: none

   http(s)://<server:port>/<lab-location>/tree

To learn more about URLs in JupyterLab and Jupyter Notebook, visit
`starting JupyterLab <http://jupyterlab.readthedocs.io/en/latest/getting_started/starting.html>`_.

``--debug`` and ``--no-build``
------------------------------

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
