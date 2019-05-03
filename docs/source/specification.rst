.. _specification:

====================================================
The Reproducible Execution Environment Specification
====================================================

repo2docker scans a repository for particular :ref:`config-files`, such
as ``requirements.txt`` or ``REQUIRE``. The collection of files, their contents,
and the resulting actions that repo2docker takes is known
as the **Reproducible Execution Environment Specification** (or REES).

The goal of the REES is to automate and encourage existing community best practices
for reproducible computational environments. This includes installing
community-standard specification files such as ``requirements.txt`` or ``REQUIRE`` using
standard tools such as ``pip`` or ``conda`` or ``apt``. While repo2docker automates the
creation of the environment, a human should be able to look at a REES-compliant
repository and reproduce the environment using common, clear steps without
repo2docker software.

Currently, the definition of the REE Specification is the following:

    Any collection of files taken from the :ref:`config-files`
    list, placed either in the root of a folder or in a sub-folder called
    either ``binder/`` or ``.binder/``.

For example, the REES recognises ``requirements.txt`` as a valid config file.
The file format is as defined by the ``requirements.txt`` standard of the Python
community. A REES-compliant tool will install a Python interpreter (of unspecified version)
and perform the equivalent action of ``pip install -r requirements.txt`` so that the
user can afterwards run python and use the packages installed.
