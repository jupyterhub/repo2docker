(languages)=

# Choose languages for your environment

You can define many different languages in your configuration files. This
page describes how to use some of the more common ones.

## Python

Your environment will have Python (and specified dependencies) installed when
you use one of the following configuration files:

- `requirements.txt`
- `environment.yml`

By default, the environment will have {{ default_python }}.

### Specify a version of Python

To specify a specific version of Python, you have two options:

- Use [environment.yml](#environment-yml). Conda environments let you define
  the Python version in `environment.yml`.
  To do so, add `python=X.X` to your dependencies section, like so:

  ```
  name: python 2.7
  dependencies:
    - python=2.7
    - numpy
  ```

- Use [runtime.txt](#runtime-txt) with [requirements.txt](#requirements-txt).
  If you are using `requirements.txt` instead of `environment.yml`,
  you can specify the Python runtime version in a separate file called `runtime.txt`.
  This file contains a single line of the following form:

  ```
  python-X.X
  ```

  For example:

  ```
  python-3.6
  ```

### Supported versions of Python

Repo2docker officially supports the following versions of Python:

- 3.11 (added in 2023)
- 3.10 (added in 2022, default in 2023)
- 3.9 (added in 2021)
- 3.8 (added in 0.11)
- 3.7 (added in 0.7, default in 0.8)
- 3.6 (default in 0.7 and earlier)
- 3.5
- 2.7

Additional versions may work, as long as the [base environment](https://github.com/jupyterhub/repo2docker/blob/HEAD/repo2docker/buildpacks/conda/environment.yml) can be installed for your version of Python.
The most likely source of incompatibility is if one of the packages in the base environment is not packaged for your Python, either because the version of the package is too new and your chosen Python is too old, or vice versa.

If an old version of Python is specified (3.6 or earlier in 2023), a separate environment for the kernel will be installed with your requested Python version.
The notebook server will run in the default {{ default_python }} environment.
That is, your _notebooks_ will run with Python 3.6, while your notebook _server_ will run with {{ default_python }}.

These two environments can be distinguished with `$NB_PYTHON_PREFIX/bin/python` for the server and `$KERNEL_PYTHON_PREFIX/bin/python` for the kernel.
Both of these environment variables area always defined, even when they are the same.

Starting in 2023, the default version of Python used when Python version is unspecified will be updated more often.
Python itself releases a new version every year now, and repo2docker will follow, with the default Python version generally trailing the latest stable version of Python itself by 1-2 versions.

If you choose not to specify a Python version, your repository is _guaranteed_ to stop working, eventually.
We **strongly** recommend specifying a Python version (in environment.yml, runtime.txt, Pipfile, etc.)

## The R Language

repo2docker supports R, the open source [RStudio IDE](https://www.rstudio.com/) as well
as Jupyter support for R with the [IRKernel](https://irkernel.github.io/). To set it up,
you need to create a `runtime.txt` file with the following format:

> r-\<version>-\<YYYY>-\<MM>-\<DD>

This will provide you R of given version (such as 4.1, 3.6, etc), and a CRAN snapshot
to install libraries from on the given date. You can install more R packages from CRAN
by adding a [install.R](#install-R) file to your repo. RStudio and IRKernel are
installed by default for all R versions.

[packagemanager.posit.co](https://packagemanager.posit.co/client/#/)
will be used to provide much faster installations via [binary packages](https://www.rstudio.com/blog/package-manager-v1-1-no-interruptions/).
For _some_ packages, this might require you install underlying system libraries
using [apt.txt](#apt-txt) - look at the page for the CRAN package you are interested in at
[packagemanager.posit.co](https://packagemanager.posit.co/client/#/) to find
a list.

repo2docker stopped using the Microsoft mirror MRAN for older R versions after its shutdown in July, 2023.

### Supported versions of R

The default version of R is currently R 4.2. You can select the version of
R you want to use by specifying it in the [runtime.txt](#runtime-txt)
file.

We support R versions 3.4, 3.5, 3.6, 4.0, 4.1 and 4.2.

## Julia

To build an environment with Julia, include a configuration file called
`Project.toml`. The format of this file is documented at
[the Julia Pkg.jl documentation](https://julialang.github.io/Pkg.jl/v1/).
To specify a specific version of Julia to install, put a Julia version in the
`[compat]` section of the `Project.toml` file, as described
here: <https://julialang.github.io/Pkg.jl/v1/compatibility/>.

### Supported versions of Julia

All Julia versions since Julia 1.3 are supported via a [Project.toml](project-toml)
file, and this is the recommended way to install Julia environments.

Julia < 1.3 and the older Julia REQUIRE file is no longer supported because required infrastructure has been removed.

## Languages not covered here

If a language is not "officially" supported by a build pack, it can often be
installed with a `postBuild` script. This will run arbitrary `bash` commands,
and can be used to download / install a language.

## Using multiple languages at once

It may also be possible to combine multiple languages in a single environment.
The details on how to accomplish this with all possible combinations are outside
the scope of this guide. However we recommend that you take a look at the
[Multi-Language Demo](https://github.com/binder-examples/multi-language-demo)
repository for some inspiration.
