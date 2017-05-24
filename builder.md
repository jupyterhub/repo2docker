# Creating a New Builder for jupyter-repo2docker

## Overview

Repo2Docker uses [s2i][] to turn a git repository into a Docker image. The
image:

- may be used with Jupyter notebooks, including via JupyterHub
- includes the contents of the source git repo

This process is handled via an [s2i][] **builder**. A builder contains two
components:

1. the **s2i builder image**, which turns GitHub repos into docker images
2. the **BuildPack object** in `repo2docker/detectors.py`, which detects
   which builder to use based on the source repo contents, and then invokes
   the appropriate, matching builder image

[s2i]: https://github.com/openshift/source-to-image/blob/master/docs/builder_image.md


## Making a new s2i builder

1. Choose a name for a new builder, `buildername`. Typically, the `buildername`
   will correspond to a package manager name.

   For example, let's choose `npm` as the `buildername`.

2. To get started creating a builder, run the `s2i create` command. From the
  `s2i-builders` directory, run:

    ```bash
    s2i create jupyterhub/repo2docker-{buildername} {buildername}

    # Example `s2i create` command where {buildername} is npm
    s2i create jupyterhub/repo2docker-npm npm
    ```

3. To build the image, in the newly created `s2i-builders/{buildername}`
   directory (or `s2i-builders/npm` directory for the example), run:

    ```bash
    make
    ```

    This step creates a `Dockerfile`.

## Modifying the Dockerfile

You can modify your `Dockerfile` and fill out the `docker build`, as you want.
There are two files that may be edited:

1. **The `Dockerfile` for the builder itself** The `Dockerfile` is used to
   create the base builder image (e.g. installing the base runtime environment).

2. **The `s2i/bin/assemble` script** The `s2i/bin/assemble` script is run
when creating each new image from a given repository (e.g. pulling in
repo-specific dependencies and repo contents).

You can view the existing s2i-builders in this repo for examples to reference.

## Adding the BuildPack

Once you builder image is finished, you need to add a Buildpack to run your
builds and to make sure that your new builder is used on the appropriate source
repos.

1. Define your BuildPack class in `detectors.py`. In most cases, you only need
  to implement two things if you subclass `S2IBuildPack`:

  - the `detect` method to determine whether a repo should choose your
    BuildPack
  - setting the `build_image`  attribute, either via config or during the
    `.detect()` method

2. Finally, to get the builder application to use your BuildPack, add it to
   the `buildpacks` list in `app.py`.

3. Once everything above is done, you should be able to build a repo by
   specifying a source repo URL with this command:

    python -m repo2docker https://github.com/yourname/your-repo
