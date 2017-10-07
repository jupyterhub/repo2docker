System - Post-build scripts
---------------------------

It is possible to run scripts after you've built the environment specified in
your other files. This could be used to, for example, download data or run
some configuration scripts. For example, this will download and install a
Jupyter extension.

.. note::

   This file needs to be executable in order to work with ``repo2docker``. If
   you're on Linux or macOS, run::

       chmod +x postBuild

   If you're on windows, you can accomplish the same behavior with this
   ``git`` command::

       git update-index --chmod=+x postBuild
