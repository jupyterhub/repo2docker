.. _specification:

====================================================
The Reproducible Execution Environment Specification
====================================================

repo2docker scans a repository for particular :ref:`config-files`, such
as ``requirements.txt`` or ``Project.toml``. The collection of files, their contents,
and the resulting actions that repo2docker takes is known
as the **Reproducible Execution Environment Specification** (or REES).

The goal of the REES is to automate and encourage existing community best practices
for reproducible computational environments. This includes installing pacakges using
community-standard specification files and their corresponding tools,
such as ``requirements.txt`` (with ``pip``), ``Project.toml`` (with Julia), or
``apt.txt`` (with ``apt``). While repo2docker automates the
creation of the environment, a human should be able to look at a REES-compliant
repository and reproduce the environment using common, clear steps without
repo2docker software.

Currently, the definition of the REE Specification is the following:

    Any directory containing zero or more files from the :ref:`config-files` list is a
    valid reproducible execution environment as defined by the REES. The
    configuration files have to all be placed either in the root of the
    directory, in a ``binder/`` sub-directory or a ``.binder/`` sub-directory.

For example, the REES recognises ``requirements.txt`` as a valid config file.
The file format is as defined by the ``requirements.txt`` standard of the Python
community. A REES-compliant tool will install a Python interpreter (of unspecified version)
and perform the equivalent action of ``pip install -r requirements.txt`` so that the
user can afterwards run python and use the packages installed.
