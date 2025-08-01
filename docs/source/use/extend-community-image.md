# Extend a community image with your own packages

If [using a community image alone](./community-image.md) doesn't provide the environment you need, you might get away with just installing one or two extra things on top of it.

To do this, you should define a `Dockerfile` that "inherits" the community image, and "extend" it to add a few extra things.

[Here's a repository that demonstrates how to do this using the `repo2docker` github action](https://github.com/2i2c-org/example-inherit-from-community-image). Below is a summary of the most important parts.

A [local `environment.yml` file](https://github.com/2i2c-org/example-inherit-from-community-image/blob/main/environment.yml) defines **only the extra things to install** in addition to the upstream image.

```{code-block}
:caption: environment.yml
channels:
  - conda-forge

dependencies:
  - jupyterhub-singleuser>=3.0,<4.0

  # Everyone wants to use nbgitpuller for everything, so let's do that
  - nbgitpuller=1.1.*
  # Install packages from pip
  - pip
  - pip:
    - otter-grader
```

A local `Dockerfile` does the following things:

- Inherits from the upstream image.
- Copies your local `environment.yml` file into a directory in the image.
- Updates the `conda` environment with it to install the extra packages.

For example, the following inherits the `scipy-notebook` image with the `2023-05-01` tag and takes the above steps. (you could follow a similar workflow with other package managers).

```{code-block} Dockerfile
:caption: Dockerfile
FROM jupyter/scipy-notebook:2023-05-01
COPY environment.yml /tmp/environment.yml
RUN mamba env update --prefix ${CONDA_DIR} --file /tmp/environment.yml
COPY image-tests image-tests
RUN ls
```

A [github workflow](https://github.com/2i2c-org/example-inherit-from-community-image/blob/main/.github/workflows/build.yaml) uses the [`repo2docker` GitHub action](#github-action) to build and push a Docker image using repo2docker. Here's an example of what the GitHub workflow looks like:

````{dropdown} Example GitHub workflow code
```{code-block} yaml
:caption: .github/workflows/build.yaml
name: Build and push container image

on:
  push:
    branches:
      - main

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    steps:

    # For biggish images, github actions runs out of disk space.
    # So we cleanup some unwanted things in the disk image, and reclaim that space for our Docker use
    # https://github.com/actions/virtual-environments/issues/2606#issuecomment-772683150
    # and https://github.com/easimon/maximize-build-space/blob/b4d02c14493a9653fe7af06cc89ca5298071c66e/action.yml#L104
    # This gives us a total of about 52G of free space, which should be enough for now
    - name: cleanup disk space
      run: |
        sudo rm -rf /usr/local/lib/android /usr/share/dotnet /opt/ghc
        df -h

    - name: Checkout files in repo
      uses: actions/checkout@main

    - name: Build and push the image to quay.io
      uses: jupyterhub/repo2docker-action@master
      with:
        # Make sure username & password/token pair matches your registry credentials
        DOCKER_USERNAME: ${{ secrets.QUAY_USERNAME }}
        DOCKER_PASSWORD: ${{ secrets.QUAY_PASSWORD }}
        DOCKER_REGISTRY: "quay.io"
        # Disable pushing a 'latest' tag, as this often just causes confusion
        LATEST_TAG_OFF: true
        #
        # Uncomment and modify the following line with your image name, otherwise no push will happen
        IMAGE_NAME: "yuvipanda/example-inherit-from-community-image"

    # Lets us monitor disks getting full as images get bigger over time
    - name: Show how much disk space is left
      run: df -h
```
````
