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
DataFrames
```

Note that `IJulia` is installed by default.

These packages will all be installed, and then precompiled via `using`.
