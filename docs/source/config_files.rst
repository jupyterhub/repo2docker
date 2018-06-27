.. _config-files:

Supported configuration files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Below is a list of supported configuration files (roughly in the order of build priority).

.. contents::
   :local:
   :depth: 1

``Dockerfile``
^^^^^^^^^^^^^^

This will be treated as a regular Dockerfile and a regular Docker build will be performed.
The presence of a Dockerfile takes priority over and ignores all other build behavior
specified in other configuration files.

In the majority of cases, providing your own Dockerfile is not necessary as the base
images provide core functionality, compact image sizes, and efficient builds. We recommend
trying the other configuration files before deciding to use your own Dockerfile.

See the `Binder Documentation <https://mybinder.readthedocs.io/en/latest/dockerfile.html>`_ for
best-practices with Dockerfiles.

``environment.yml``
^^^^^^^^^^^^^^^^^^^

This is a conda environment specification, that lets you install packages with conda.
You can also install files from pip in your ``environment.yml`` as well.
Our example `enviornment.yml <https://github.com/binder-examples/python-conda_pip/blob/master/environment.yml>`_
shows how one can specify a conda environment for repo2docker.

``requirements.txt``
^^^^^^^^^^^^^^^^^^^^

This specifies a list of Python packages that should be installed in your
 environment. Our `requirements.txt example <https://github.com/binder-examples/requirements/blob/master/requirements.txt>`_
on GitHub shows a typical requirements file.

``REQUIRE``
^^^^^^^^^^^

This specifies a list of Julia packages. Repositories with a  ``REQUIRE`` file
**must also contain an** ``environment.yml`` **file**.  To see an example of a
Julia repository with ``REQUIRE`` and ``environment.yml``,
visit `binder-examples/julia-python <https://github.com/binder-examples/julia-python>`_.

``install.R``
^^^^^^^^^^^^^

This is used to install R libraries pinned to a specific snapshot on
`MRAN <https://mran.microsoft.com/documents/rro/reproducibility>`_.
To set the date of the snapshot add a runtime.txt_.
For an example ``install.R`` file, visit our `example install.R file <https://github.com/binder-examples/r/blob/master/install.R>`_.

``apt.txt``
^^^^^^^^^^^

A list of Debian packages that should be installed. The base image used is usually the latest released
version of Ubuntu.

We use ``apt.txt``, for example, to install LaTeX in our
`example apt.txt for LaTeX <https://github.com/binder-examples/latex/blob/master/apt.txt>`_.


``setup.py``
^^^^^^^^^^^^

To install your repository like a Python package, you may include a
``setup.py`` file. repo2docker installs ``setup.py`` files by running
``pip install -e .``.
While one can specify dependencies in ``setup.py``,
repo2docker **requires configuration files such as** ``environment.yml`` or
``requirements.txt``

``postBuild``
^^^^^^^^^^^^^

A script that can contain arbitrary commands to be run after the whole repository has been built. If you
want this to be a shell script, make sure the first line is ```#!/bin/bash``.

An example usecase of ``postBuild`` file is JupyterLab's demo on mybinder.org.
It uses a ``postBuild`` file in a folder called ``binder`` to `prepare
their demo for binder <https://github.com/jupyterlab/jupyterlab-demo/blob/master/binder/postBuild>`_.

.. _runtime.txt:

``runtime.txt``
^^^^^^^^^^^^^^^

This allows you to control the runtime of Python or R.

Adding ``python-2.7`` in the file our repository will run in a virtualenv with
Python 2 installed. To see a full example repository, visit our
`Python2 example <https://github.com/binder-examples/python2_runtime/blob/master/runtime.txt>`_.

repo2docker uses R libraries pinned to a specific snapshot on
`MRAN <https://mran.microsoft.com/documents/rro/reproducibility>`_.
You need to have a runtime.txt file that is formatted as
``r-<YYYY>-<MM>-<DD>``, where YYYY-MM-DD is a snapshot at MRAN that will be
used for installing libraries.

To see an example R repository, visit our `R
example in binder-examples <https://github.com/binder-examples/r/blob/master/runtime.txt>`_.
