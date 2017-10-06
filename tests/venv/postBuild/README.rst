System - Post-build scripts
---------------------------

It is possible to run scripts after you've built the environment specified in
your other files. This could be used to, for example, download data or run
some configuration scripts. For example, this will download and install a
Jupyter extension.

.. note::

   This file needs to be executable in order to work with ``repo2docker``. The
   easiest way to do this is to run the following command with ``git``::

       git update-index --chmod=+x postBuild
