# Configuration for datascience workflows

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
For example, see the [binder-examples environment.yml](https://github.com/binder-examples/python-conda_pip/blob/HEAD/environment.yml)
file.
:::

You can also specify which Python version to install in your built environment
with `environment.yml`. By default, `repo2docker` installs
{{ default_python }} with your `environment.yml` unless you include the version of
Python in this file. `conda` Should support all versions of Python,
though `repo2docker` support is best with Python 3.7-3.11.

:::{warning}
If you include a Python version in a `runtime.txt` file in addition to your
`environment.yml`, your `runtime.txt` will be ignored.
:::

(require)=

## `REQUIRE` - Install a Julia environment (legacy)

`REQUIRE` files no longer work, and are no longer supported.
The recommended way of installing a Julia environment is to use a `Project.toml` file.

(install-r)=

## `install.R` - Install an R/RStudio environment

This is used to install R libraries pinned to a specific snapshot on
[Posit Package Manager](https://packagemanager.posit.co/).
To set the date of the snapshot add a [runtime.txt].
For an example `install.R` file, visit our [example install.R file](https://github.com/binder-examples/r/blob/HEAD/install.R).

(description)=

## `DESCRIPTION` - Install an R package

To install your repository like an R package, you may include a
`DESCRIPTION` file. repo2docker installs the package and dependencies
from the `DESCRIPTION` by running `devtools::install_local(getwd())`.

You can also have have a `runtime.txt` file that is formatted as
`r-<YYYY>-<MM>-<DD>`, where YYYY-MM-DD is a snapshot of CRAN that will be used
for your R installation. If `runtime.txt` isn't provided in this case, a
recent date will be used.
