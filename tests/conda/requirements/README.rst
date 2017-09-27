Conda - Mixed Requirements
--------------------------

An ``environment.yml`` takes precedence over ``requirements.txt``.
To install Python packages into a conda environment with pip, use the ``pip`` key in ``environment.yml``:

.. sourcecode:: yaml

    dependencies:
      - numpy
      - pip:
        - tornado
