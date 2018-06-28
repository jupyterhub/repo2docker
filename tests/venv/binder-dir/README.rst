Binder Directory for configuration files
----------------------------------------

If  a directory called ``binder/`` exists in the top level of the repository,
then all configuration files that are **not** in ``binder/`` will be ignored.
This is particularly useful if you have a ``Dockerfile`` defined in a
repository, but don't want ``repo2docker``to use it for building the
environment.
