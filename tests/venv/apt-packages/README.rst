System - APT Packages
---------------------

It is possible to install packages using the Shell with the ``apt.txt`` file.
This allows you to install libraries that aren't easy to install with package
managers such as ``pip`` or ``conda``. This can be useful if you must install
something that depends on a low-level library already being present.

In this case we install ``gfortran``, which does not have an easy Python
install.
