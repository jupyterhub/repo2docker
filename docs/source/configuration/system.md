# System-wide configuration

(apt-txt)=

## `apt.txt` - Install packages with apt-get

A list of Debian packages that should be installed. The base image used is usually the latest released
version of Ubuntu.

We use `apt.txt`, for example, to install LaTeX in our
[example apt.txt for LaTeX](https://github.com/binder-examples/latex/blob/HEAD/apt.txt).

(runtime-txt)=

## `runtime.txt` - Specifying runtimes

Sometimes you want to specify the version of the runtime (e.g. the version of Python or R), but the environment specification format will not let you specify this information (e.g. `requirements.txt` or `install.R`).
For these cases, we have a special file, `runtime.txt`.

:::{warning}
`runtime.txt` is only supported when used with environment specifications
that do not already support specifying the runtime
(when using [`environment.yml`](#environment-yml) for conda or [`Project.toml`](#project-toml) for Julia, `runtime.txt` will be ignored).
:::

### Set the Python version

Add the line `python-x.y` in `runtime.txt` to run the repository with Python version x.y.
See our [Python2 example repository](https://github.com/binder-examples/python2_runtime/blob/HEAD/runtime.txt).

### Set the R version

Add the line `r-<RVERSION>-<YYYY>-<MM>-<DD>` in `runtime.txt` to run the repository with R version `RVERSION` and libraries from a `YYYY-MM-DD` snapshot of the [Posit Package Manager](https://packagemanager.posit.co/client/#/repos/2/overview).

`RVERSION` can be set to 3.4, 3.5, 3.6, or to patch releases for the 3.5 and 3.6 series.
If you do not specify a version, the latest release will be used.

See our [R example repository](https://github.com/binder-examples/r/blob/HEAD/runtime.txt).

(default-nix)=

## `default.nix` - the nix package manager

Specify packages to be installed by the [nix package manager](https://github.com/NixOS/nixpkgs).
When you use this config file all other configuration files (like `requirements.txt`)
that specify packages are ignored. When using `nix` you have to specify all
packages and dependencies explicitly, including the Jupyter notebook package that
`repo2docker` expects to be installed. If you do not install Jupyter explicitly
`repo2docker` will no be able to start your container.

[nix-shell](https://nixos.org/nix/manual/#sec-nix-shell) is used to evaluate
a `nix` expression written in a `default.nix` file. Make sure to
[pin your nixpkgs](https://discourse.nixos.org/t/nixops-pinning-nixpkgs/734)
to produce a reproducible environment.

To see an example repository visit
[nix binder example](https://github.com/binder-examples/nix).

(dockerfile)=

## `Dockerfile` - Advanced environments

In the majority of cases, providing your own `Dockerfile` is not necessary as the base images provide core functionality, compact image sizes, and efficient builds. We recommend trying the other configuration files before deciding to use your own `Dockerfile`.

With `Dockerfile`s, a regular Docker build will be performed.

:::{warning}
If a Dockerfile is present, all other configuration files will be ignored.
:::

See the [Advanced Binder Documentation](https://mybinder.readthedocs.io/en/latest/tutorials/dockerfile.html) for
best-practices with Dockerfiles.
