Python 3.10 (latest), and an ignored requirements file
------------------------------------------------------

The reasons for testing 3.10 specifically is that it is the latest version of
Python 3 supported by repo2docker's conda buildpack. See
``repo2docker/buildpacks/conda`` for details.

An ``environment.yml`` file takes precedence over ``requirements.txt``.
To install Python packages into a conda environment with pip, use the
``pip`` key in ``environment.yml``:

.. sourcecode:: yaml

   dependencies:
     - numpy
     - pip:
       - tornado
