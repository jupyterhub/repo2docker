(config-files)=

# Configuration files supported by repo2docker

`repo2docker` looks for configuration files in the repository being built
to determine how to build it. In general, `repo2docker` uses the same
configuration files as other software installation tools,
rather than creating new custom configuration files.

:::{seealso}
The [binder examples](https://github.com/binder-examples) organization on
GitHub contains a list of sample repositories for common configurations
that `repo2docker` can build with various configuration files such as
Python and R installation in a repository.
:::

A list of supported configuration files (roughly in the order of build priority)
can be found on this page (and to the right).

```{toctree}
:maxdepth: 2
./research
./development
./system
./actions
```
