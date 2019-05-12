Python - Pipfile(.lock) + environment.yml
-----------------------------------------

We should ignore the ``Pipfile`` or ``Pipfile.lock`` if there is an
``environment.yml`` alongside it. Conda can install more things than ``pip`` or
``pipenv`` can so we would limit ourselves if we prioritized the ``Pipfile``s.
