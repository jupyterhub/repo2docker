R environment - install.R
-------------------------

You can install an R environment with the following two files:

* ``install.R``: a script that will be run from an R installation. This is
  generally used to install and set up packages.
* ``runtime.txt``: include a line that specifies a date for the appropriate
  MRAN repository version for packages. It should have the structure
  ``r-YYYY-MM-DD``.
