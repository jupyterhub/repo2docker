(faq)=

# Frequently Asked Questions (FAQ)

A collection of frequently asked questions with answers. If you have a question
and have found an answer, send a PR to add it here!

## Why is my repository failing to build with `ResolvePackageNotFound` ?

If you used `conda env export` to generate your `environment.yml` it will generate a list of packages and versions of packages that is pinned to platform specific versions.
These very specific versions are not available in the Linux Docker image used by `repo2docker`. A typical error message will look like the following:

```
Step 39/44 : RUN conda env update -n root -f "environment.yml" && conda clean -tipsy && conda list -n root
---> Running in ebe9a67762e4
Solving environment: ...working... failed

ResolvePackageNotFound:
- jsonschema==2.6.0=py36hb385e00_0
- libedit==3.1.20181209=hb402a30_0
- tornado==5.1.1=py36h1de35cc_0
...
```

We recommend to use `conda env export --no-builds -f environment.yml` to export
your environment and then edit the file by hand to remove platform specific
packages like `appnope`.

See {ref}`export-environment` for a recipe on how to create strict exports of
your environment that will work with `repo2docker`.

## Can I add executable files to the user's PATH?

Yes! With a [](#postBuild) file, you can place any files that should be called from the command line in the folder `~/.local/bin`.
This folder will be available in a user's PATH, and can be run from the command line (or as a subsequent build step.)

## Can I use repo2docker to bootstrap my own `Dockerfile` to edit by hand?

No, you can't.

If you pass the `--debug` flag to `repo2docker`, it outputs the
intermediate `Dockerfile` that is used to build the Docker image. While
it is tempting to copy this as a base for your own `Dockerfile`, that is
not supported & in most cases will not work. The `--debug` output is
just our intermediate generated `Dockerfile`, and is meant to be built
in a very specific way. Hence the output of `--debug` can not be
built with a normal `docker build -t .` or similar traditional
Docker command.

Check out the [binder-examples](http://github.com/binder-examples/) GitHub
organization for example repositories you can copy & modify for your own use!

## Can I use repo2docker to edit a local host repository within a Docker environment?

Yes: use the `--editable` or `-E` flag (don't confuse this with
the `-e` flag for environment variables), and run repo2docker on a
local repository:

```
repo2docker -E my-repository/
```

This builds a Docker container from the files in that repository
(using, for example, a `requirements.txt` or `install.R` file),
then runs that container, while connecting the working directory
inside the container to the local repository outside the
container. For example, in case there is a notebook file (`.ipynb`),
this will open in a local web browser, and one can edit it and save
it. The resulting notebook is updated in both the Docker container and
the local repository. Once the container is exited, the changed file
will still be in the local repository.

This allows for easy testing of the container while debugging some
items, as well as using a fully customizable container to edit
notebooks (among others).

:::{note}
Editable mode is a convenience option that will bind the
repository to the container working directory (usually
`$HOME`). If you need to mount to a different location in
the container, use the `--volumes` option instead. Similarly,
for a fully customized user Dockerfile, this option is not
guaranteed to work.
:::

## Why is my R shiny app not launching?

If you are trying to run an R shiny app using the `/shiny/folder_containing_shiny`
url option, but the launch returns "The application exited during initialization.",
there might be something wrong with the specification of the app. One way of debugging
the app in the container is by running the `rstudio` url, open either the ui or
server file for the app, and run the app in the container rstudio. This way you can
see the rstudio logs as it tries to initialize the shiny app. If you are missing a
package or other dependency for the container, this will be obvious at this stage.

## Why does repo2docker need to exist? Why not use tool like source2image?

The Jupyter community believes strongly in building on top of pre-existing tools whenever
possible (this is why repo2docker buildpacks largely build off of patterns that already
exist in the data analytics community). We try to perform due-diligence and search for
other communities to leverage and help, but sometimes it makes the most sense to build
our own new tool. In the case of repo2docker, we spent time integrating with a pre-existing
tool called [source2image](https://github.com/openshift/source-to-image/).
This is an excellent open tool for containerization, but we
ultimately decided that it did not fit the use-case we wanted to address. For more information,
read our [blog post about why we built repo2docker](https://github.com/yuvipanda/words/blob/fd096dd49d87e624acd8bdf6d13c0cecb930bb3f/content/post/why-not-s2i.md).
