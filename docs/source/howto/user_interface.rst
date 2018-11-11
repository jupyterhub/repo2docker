.. _user_interface:

============================
Configure the user interface
============================

You can build several user interfaces into the resulting Docker image.
This is controlled with various :ref:`configuration files <config-files>`.

JupyterLab
----------

You do not need any extra configuration in order to allow the use
of the JupyterLab interface. You can launch JupyterLab from within a user
session by opening the Jupyter Notebook and appending ``/lab`` to the end of the URL
like so:

.. code-block:: none

   http(s)://<server:port>/lab

To switch back to the classic notebook, add ``/tree`` to the URL like so:

.. code-block:: none

   http(s)://<server:port>/tree

To learn more about URLs in JupyterLab and Jupyter Notebook, visit
`starting JupyterLab <http://jupyterlab.readthedocs.io/en/latest/getting_started/starting.html>`_.

RStudio
-------

The RStudio user interface is automatically enabled if a configuration file for
R is detected (i.e. an R version specified in ``runtime.txt``). If this is detected,
RStudio will be accessible by appending ``/rstudio`` to the URL, like so:

.. code-block:: none

   http(s)://<server:port>/rstudio

Stencila
--------

The Stencila user interface is automatically enabled if a Stencila document (i.e. 
a file `manifest.xml`) is detected. Stencila will be accessible by appending 
``/stencila`` to the URL, like so:

.. code-block:: none

   http(s)://<server:port>/stencila

The editor will open the Stencila document corresponding to the last `manifest.xml`
found in the file tree. If you want to open a different document, you can configure
the path in the URL parameter `archive`:

.. code-block:: none

   http(s)://<server:port>/stencila/?archive=other-dir
