System - Specifying runtime environments
----------------------------------------

You can specify runtime environments (such as Python 2 or 3) with a
``runtime.txt`` file. To do so, include a line of the following form in
your ``runtime.txt`` file:

```
python-N
```

Where ``N`` is either ``2`` or ``3``. If ``N==2``, Python 2.7 will be used.
If ``N==3``, Python 3.6 will be used.

This is an example that selects Python 3. Currently you can not use
this to select a specific version of Python 3 (e.g. 3.4 vs 3.6). If you
need this level of control we recommend you use a `environment.yml`.

Note that you can also install Python environments using the Anaconda
distribution by using an ``environment.yml`` file.
