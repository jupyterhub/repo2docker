.. _user_interface:

============================
Configure the user interface
============================

You can build several user interfaces into the resulting Docker image.
This is controlled with various :ref:`configuration files <config-files>`.


JupyterLab
==========

JupyterLab is the default interface for repo2docker.

The following Binder URL will open the
`pyTudes repository <https://github.com/norvig/pytudes>`_
and begin a JupyterLab session in the ``ipynb`` folder:

https://mybinder.org/v2/gh/norvig/pytudes/HEAD?urlpath=lab/tree/ipynb

The ``/tree/ipynb`` above is how JupyterLab directs you to a specific file
or folder.

To learn more about URLs in JupyterLab and Jupyter Notebook, visit
`starting JupyterLab <http://jupyterlab.readthedocs.io/en/latest/getting_started/starting.html>`_.

Classic Notebook Interface
==========================

The classic notebook is also available without any configuration.
To switch to the classic notebook,
You do not need any extra configuration in order to allow the use
of the classic notebook interface.
You can launch the classic notebook interface from within a user
session by opening JupyterLab and replacing ``/lab/`` with ``/tree/`` in the default juptyerlab URL
like so:

.. code-block:: none

   http(s)://<server:port>/tree/

And you can switch back to JupyterLab by replacing ``/tree/`` with ``/lab/``:

.. code-block:: none

   http(s)://<server:port>/lab/


nteract
=======

`nteract is a notebook interface <https://nteract.io/>`_ built with React.
It is similar to a more feature-filled version of the traditional
Jupyter Notebook interface.

nteract comes pre-installed in any session that has been built from
a Python repository.

You can launch nteract from within a user
session by replacing ``/tree`` with ``/nteract`` at the end of a notebook
server's URL like so:

.. code-block:: none

   http(s)://<server:port>/nteract

For example, the following Binder URL will open the
`pyTudes repository <https://github.com/norvig/pytudes>`_
and begin an nteract session in the ``ipynb`` folder:

https://mybinder.org/v2/gh/norvig/pytudes/HEAD?urlpath=nteract/tree/ipynb

The ``/tree/ipynb`` above is how nteract directs you to a specific file
or folder.

To learn more about nteract, visit `the nteract website <https://nteract.io/about>`_.


RStudio
=======

The RStudio user interface is automatically enabled if a configuration file for
R is detected (i.e. an R version specified in ``runtime.txt``). If this is detected,
RStudio will be accessible by appending ``/rstudio`` to the URL, like so:

.. code-block:: none

   http(s)://<server:port>/rstudio

For example, the following Binder link will open an RStudio session in
the `R demo repository <https://github.com/binder-examples/r>`_.

http://mybinder.org/v2/gh/binder-examples/r/HEAD?urlpath=rstudio


Shiny
=====

`Shiny lets you create interactive visualizations with R <https://shiny.rstudio.com/>`_.
Shiny is automatically enabled if a configuration file for
R is detected (i.e. an R version specified in ``runtime.txt``). If
this is detected, Shiny will be accessible by appending
``/shiny/<folder-w-shiny-files>`` to the URL, like so:

.. code-block:: none

   http(s)://<server:port>/shiny/bus-dashboard

This assumes that a folder called ``bus-dashboard`` exists in the root
of the repository, and that it contains all of the files needed to run
a Shiny app.

For example, the following Binder link will open a Shiny session in
the `R demo repository <https://github.com/binder-examples/r>`_.

http://mybinder.org/v2/gh/binder-examples/r/HEAD?urlpath=shiny/bus-dashboard/


Stencila
========

.. note::

   Stencila support has been removed due to changes in stencila making it incompatible.
   Please `get in touch <https://discourse.jupyter.org>`__ if you would like to help restore stencila support.
