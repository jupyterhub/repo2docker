Julia - REQUIRE: packages and julia version number
---------------

To specify dependencies in Julia, include a REQUIRE file.

To specify a version of Julia to be installed, the first line of the file must
follow the format `julia <version-number>`. For example:
```
julia 0.7
```

To add package dependencies, the rest of the file can include lines that list
the names of packages you'd like to be installed. For example:

```
PyPlot
IJulia
DataFrames
```

Each one will be installed but **not** pre-compiled. If you'd like to
pre-compile your Julia packages, consider using a ``postBuild`` file.

Note that this example also specifies Python dependencies with an
``environment.yml`` file.
