Python - pyproject.toml with python_version and runtime.txt
-----------------------------------------------------------

We are ignoring the runtime.txt if there is a pyproject.toml or poetry.lock
available. And since `python_version = "3.8"` in pyproject.toml, the `python-3.7`
in runtime.txt should be ignored. Is it?
