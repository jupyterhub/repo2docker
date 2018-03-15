.. _install:

Installing ``repo2docker``
==========================

Prerequisite: docker
--------------------

Install `Docker <https://www.docker.com>`_ as it is required to build Docker images.

Installing with ``pip``
-----------------------

We recommend installing ``repo2docker`` with the ``pip`` tool::

    python3 -m pip install jupyter-repo2docker

For infomation on using ``repo2docker``, see :ref:`usage`.

Installing from source code
---------------------------

Alternatively, you can install repo2docker from source,
i.e. if you are contributing back to this project::

  git clone https://github.com/jupyter/repo2docker.git
  cd repo2docker
  pip install -e .

That's it! For information on using ``repo2docker``, see
:ref:`usage`.

Note about Windows support
--------------------------

Windows support by ``repo2docker`` is still in the experimental stage. 

An article about `using Windows and the WSL`_ (Windows Subsytem for Linux or
Bash on Windows) provides additional information about Windows and docker.


.. _using Windows and the WSL: https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly
