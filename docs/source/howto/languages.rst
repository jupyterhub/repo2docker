.. _languages:

=====================================
Choose languages for your environment
=====================================

You can define many different languages in your configuration files. This
page describes how to use some of the more common ones.

Python
======

Your environment will have Python (and specified dependencies) installed when
you use one of the following configuration files:

* ``requirements.txt``
* ``environment.yml``

.. note::

  By default, the environment will have |default_python|.

.. versionchanged:: 0.8

  Upgraded default Python from 3.6 to 3.7.


Specifying a version of Python
------------------------------

To specify a specific version of Python, you have two options:

* Use :ref:`environment.yml <environment.yml>`. Conda environments let you define
  the Python version in ``environment.yml``.
  To do so, add ``python=X.X`` to your dependencies section, like so::

    name: python 2.7
    dependencies:
      - python=2.7
      - numpy

* Use :ref:`runtime.txt <runtime.txt>` with :ref:`requirements.txt <requirements.txt>`.
  If you are using ``requirements.txt`` instead of ``environment.yml``,
  you can specify the Python runtime version in a separate file called ``runtime.txt``.
  This file contains a single line of the following form::

    python-X.X

  For example::

    python-3.6


The R Language
==============

repo2docker supports  R, the open source `RStudio IDE <https://www.rstudio.com/>`_ as well
as Jupyter support for R with the `IRKernel <https://irkernel.github.io/>`_. To set it up,
you need to create a ``runtime.txt`` file with the following format:

  r-<version>-<YYYY>-<MM>-<DD>

This will provide you R of given version (such as 4.1, 3.6, etc), and a CRAN snapshot
to install libraries from on the given date. You can install more R packages from CRAN
by adding a :ref:`install.R<install.R>` file to your repo. RStudio and IRKernel are
installed by default for all R versions.

`packagemanager.posit.co <https://packagemanager.posit.co/client/#/>`_
will be used to provide much faster installations via `binary packages <https://www.rstudio.com/blog/package-manager-v1-1-no-interruptions/>`_.
For *some* packages, this might require you install underlying system libraries
using :ref:`apt.txt` - look at the page for the CRAN package you are interested in at
`packagemanager.posit.co <https://packagemanager.posit.co/client/#/>`_ to find
a list.

repo2docker stopped using the Microsoft mirror MRAN for older R versions after its shutdown in July, 2023.


Julia
=====

To build an environment with Julia, include a configuration file called
``Project.toml``. The format of this file is documented at
`the Julia Pkg.jl documentation <https://julialang.github.io/Pkg.jl/v1/>`_.
To specify a specific version of Julia to install, put a Julia version in the
``[compat]`` section of the ``Project.toml`` file, as described
here: https://julialang.github.io/Pkg.jl/v1/compatibility/.

Languages not covered here
==========================

If a language is not "officially" supported by a build pack, it can often be
installed with a ``postBuild`` script. This will run arbitrary ``bash`` commands,
and can be used to download / install a language.

Using multiple languages at once
================================

It may also be possible to combine multiple languages in a single environment.
The details on how to accomplish this with all possible combinations are outside
the scope of this guide. However we recommend that you take a look at the
`Multi-Language Demo <https://github.com/binder-examples/multi-language-demo>`_
repository for some inspiration.
