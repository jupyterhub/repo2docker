Julia - REQUIRE
---------------

To specify dependencies in Julia, include a REQUIRE file that lists the names
of packages you'd like to be installed. For example:

```
PyPlot
IJulia
DataFrames
```

Each one will be installed but **not** pre-compiled. If you'd like to
pre-compile your Julia packages, consider using a ``postBuild`` file.

Note that this example also specifies Python dependencies with an
``requirements.txt`` file.
