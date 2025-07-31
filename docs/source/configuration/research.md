# Configuration for research and data science workflows

(environment-yml)=

## `environment.yml` - Install a conda environment

`environment.yml` is the standard configuration file used by [conda](https://conda.io)
that lets you install any kind of package,
including Python, R, and C/C++ packages.
`repo2docker` does not use your `environment.yml` to create and activate a new conda environment.
Rather, it updates a base conda environment [defined here](https://github.com/jupyterhub/repo2docker/blob/HEAD/repo2docker/buildpacks/conda/environment.yml) with the packages listed in your `environment.yml`.
This means that the environment will always have the same default name, not the name
specified in your `environment.yml`.

:::{note}
You can install files from pip in your `environment.yml` as well.
For example, see the [binder-examples environment.yml](https://github.com/binder-examples/python-conda_pip/blob/HEAD/environment.yml) file. See [the `conda` environment management instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-file-manually) for more information.
:::

You can also specify which Python version to install in your built environment with `environment.yml`.
By default, `repo2docker` installs {{ default_python }} with your `environment.yml` unless you include the version of Python in the `environment.yml` of your Git repository.
`conda` should support all versions of Python, though `repo2docker` support is best with `Python 3.7-3.11`.

:::{warning}
If you include a Python version in a `runtime.txt` file in addition to your
`environment.yml`, your `runtime.txt` will be ignored.
:::

(install-r)=

## `install.R` - Install packages with R/RStudio

This is used to install R libraries pinned to a specific snapshot on
[Posit Package Manager](https://packagemanager.posit.co/).
For an example `install.R` file, visit our [example `install.R` file](https://github.com/binder-examples/r/blob/HEAD/install.R).

To set the date of the snapshot, or to specify a specific version of R, add a [runtime.txt](#runtime-txt).

(description)=

## `DESCRIPTION` - Install an R package

To install your repository like an R package, you may include a `DESCRIPTION` file.
`repo2docker` installs the package and dependencies from the `DESCRIPTION` by running `devtools::install_local(getwd())`.

To define the date of the package manager snapshot, add a line to [`runtime.txt`](#runtime-txt) like so:

```
r-<YYYY>-<MM>-<DD>
```

Where `YYYY-MM-DD` is a snapshot of [CRAN](https://cran.r-project.org/) that will be used for your R installation.
If `runtime.txt` isn't provided in this case, the most recent date on CRAN will be used.

(project-toml)=

## `Project.toml` - Install a Julia environment

A `Project.toml` (or `JuliaProject.toml`) file can specify both the
version of Julia to be used and a list of Julia packages to be installed.
If a `Manifest.toml` is present, it will determine the exact versions
of the Julia packages that are installed.

:::{admonition} `REQUIRE` files are no longer supported
The recommended way of installing a Julia environment is to use a `Project.toml` file.
:::