Python - pyproject.toml (poetry.lock) + environment.yml
-------------------------------------------------------

We should ignore the ``pyproject.toml`` or ``poetry.lock`` if there is an
``environment.yml`` alongside it. Conda can install more things than ``pip`` or
can so we would limit ourselves if we prioritized the ``Pipfile``s.
