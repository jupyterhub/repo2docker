.. _faq:

Frequently Asked Questions (FAQ)
================================

A collection of frequently asked questions with answers. If you have a question
and have found an answer, send a PR to add it here!

How should I specify another version of Python?
-----------------------------------------------

One can specify a Python version in the ``environment.yml`` file of a repository
or ``runtime.txt`` file if using ``requirements.txt`` instead of ``environment.yml``.

What versions of Python (or R or Julia...) are supported?
---------------------------------------------------------

Python
~~~~~~

Repo2docker officially supports the following versions of Python
(specified in your :ref:`environment.yml <environment.yml>` or
:ref:`runtime.txt <runtime.txt>` file):

- 3.7 (added in 0.7, default in 0.8)
- 3.6 (default in 0.7 and earlier)
- 3.5
- 2.7

Additional versions may work, as long as the
`base environment <https://github.com/jupyter/repo2docker/blob/master/repo2docker/buildpacks/conda/environment.yml>`_
can be installed for your version of Python.
The most likely source of incompatibility is if one of the packages
in the base environment is not packaged for your Python,
either because the version of the package is too new and your chosen Python is too old,
or vice versa.

I Python 2.7 is specified, a separate environment for the kernel will be
installed with Python 2. The notebook server will run in the default Python 3.6
environment.

Julia
~~~~~

All Julia versions since Julia 0.7.0 are supported via a :ref:`Project.toml <Project.toml>`
file, and this is the recommended way to install Julia environments.
Julia versions 0.6.x and earlier are supported via a :ref:`REQUIRE <REQUIRE>` file.

R
~

Only R 3.4.4 is currently supported, which is installed via ``apt`` from the
`ubuntu bionic repository <https://packages.ubuntu.com/bionic/r-base>`_.




Why is my repository is failing to build with ``ResolvePackageNotFound`` ?
--------------------------------------------------------------------------

If you used ``conda env export`` to generate your ``environment.yml`` it will
generate a list of packages and versions of packages that is pinned to platform
specific versions. These very specific versions are not available in the linux
docker image used by ``repo2docker``. A typical error message will look like
the following::

  Step 39/44 : RUN conda env update -n root -f "environment.yml" && conda clean -tipsy && conda list -n root
  ---> Running in ebe9a67762e4
  Solving environment: ...working... failed

  ResolvePackageNotFound:
  - jsonschema==2.6.0=py36hb385e00_0
  - libedit==3.1.20181209=hb402a30_0
  - tornado==5.1.1=py36h1de35cc_0
  ...

We recommend to use ``conda env export --no-builds -f environment.yml`` to export
your environment and then edit the file by hand to remove platform specific
packages like ``appnope``.

See :ref:`export-environment` for a recipe on how to create strict exports of
your environment that will work with ``repo2docker``.


Can I add executable files to the user's PATH?
----------------------------------------------

Yes! With a :ref:`postBuild` file, you can place any files that should be called
from the command line in the folder ``~/.local/``. This folder will be
available in a user's PATH, and can be run from the command line (or as
a subsequent build step.)

How do I set environment variables?
-----------------------------------

To configure environment variables for all users of a repository use the
:ref:`start <start>` configuration file.

When running repo2docker locally you can use the ``-e`` or ``--env`` command-line
flag for each variable that you want to define.

For example ``jupyter-repo2docker -e VAR1=val1 -e VAR2=val2 ...``

Can I use repo2docker to bootstrap my own Dockerfile?
-----------------------------------------------------

No, you can't.

If you pass the ``--debug`` flag to ``repo2docker``, it outputs the
intermediate Dockerfile that is used to build the docker image. While
it is tempting to copy this as a base for your own Dockerfile, that is
not supported & in most cases will not work. The ``--debug`` output is
just our intermediate generated Dockerfile, and is meant to be built
in a very specific way.  Hence the output of ``--debug`` can not be
built with a normal ``docker build -t .`` or similar traditional
docker command.

Check out the `binder-examples <http://github.com/binder-examples/>`_ GitHub
organization for example repositories you can copy & modify for your own use!

Can I use repo2docker to edit a local host repository within a Docker environment?
----------------------------------------------------------------------------------

Yes: use the ``--editable`` or ``-E`` flag (don't confuse this with
the ``-e`` flag for environment variables), and run repo2docker on a
local repository::

  repo2docker -E my-repository/

This builds a Docker container from the files in that repository
(using, for example, a ``requirements.txt`` or ``install.R`` file),
then runs that container, while connecting the working directory
inside the container to the local repository outside the
container. For example, in case there is a notebook file (``.ipynb``),
this will open in a local webbrowser, and one can edit it and save
it. The resulting notebook is updated in both the Docker container and
the local repository. Once the container is exited, the changed file
will still be in the local repository.

This allows for easy testing of the container while debugging some
items, as well as using a fully customizable container to edit
notebooks (among others).


Why is my R shiny app not launching?
----------------------------------------------------------------------------------

If you are trying to run an R shiny app using the ``/shiny/folder_containing_shiny``
url option, but the launch returns "The application exited during initialization.",
there might be something wrong with the specification of the app. One way of debugging
the app in the container is by running the ``rstudio`` url, open either the ui or 
server file for the app, and run the app in the container rstudio. This way you can 
see the rstudio logs as it tries to initialise the shiny app. If you a missing a 
package or other dependency for the container, this will be obvious at this stage.

.. note::

    Editable mode is a convenience option that will bind the
    repository to the container working directory (usually
    ``$HOME``). If you need to mount to a different location in
    the container, use the ``--volumes`` option instead. Similarly,
    for a fully customized user Dockerfile, this option is not
    guaranteed to work.
