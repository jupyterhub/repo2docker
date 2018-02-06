R environment - install.R
-------------------------

You can install an R, RStudio, and IRKernel environment with the following
two files:

*  A ``runtime.txt`` file with the text::

       r-YYYY-MM-DD

   Where 'YYYY', 'MM' and 'DD' refer to a specific
   date snapshot of https://mran.microsoft.com/timemachine
   from which libraries will be installed.
*  An optional ``install.R`` file that will be executed at build time and can
   be used for installing packages from both MRAN and GitHub.

The presence of ``runtime.txt`` is enough to set up R, RStudio, and IRKernel. It
uses the ``r-base`` package from the Ubuntu apt repositories to install
R itself.
