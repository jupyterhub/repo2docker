.. _specification:

====================================================
The Reproducible Execution Environment Specification
====================================================

repo2docker scans a repository for particular :ref:`config_files`, such
as ``requirements.txt`` or ``REQUIRE``. The collection of files and their contents
that repo2docker uses is known as the **Reproducible Execution Environment Specification**.

The goal of the REE Specification is to provide a structure that is clearly-defined and that
can be extended to accomodate more components of a reproducible workflow.

Currently, the definition of the REE Specification is the following:

> Any collection of files taken from the :ref:`config_files`
> list, placed either in the root of a folder or in a sub-folder called either ``binder/`` or ``.binder/``.

In the future, the repo2docker team plans to formalize this specification into a pattern
that can also be followed in other ways, such as by creating a JSON or YAML file.