# Get started

This tutorial guides you through installing `repo2docker` and building your first environment image.

(install)=

## Install `repo2docker`

repo2docker requires Python 3.6 or above on Linux and macOS.

:::{admonition} Windows support is experimental

This [article about using Windows and the WSL](https://nickjanetakis.com/blog/setting-up-docker-for-windows-and-wsl-to-work-flawlessly) (Windows Subsytem for Linux or
Bash on Windows) provides additional information about Windows and Docker.
:::

### Prerequisite: Install Docker

Install [Docker](https://www.docker.com), as it is required to build Docker images.
The [Community Edition](https://docs.docker.com/install/) is available for free.

Recent versions of Docker are recommended.

### Install `repo2docker` with `pip`

We recommend installing `repo2docker` with the `pip` tool:

```
python3 -m pip install jupyter-repo2docker
```

(usage)=

## Build a repository with `repo2docker`

Now that you've installed Docker and `repo2docker`, we can build a repository.
To do so, follow these steps.

### Start Docker

Follow the [instructions for starting Docker](https://docs.docker.com/engine/daemon/start/) to start a Docker process.

### Build an image from a URL

Next we'll build a reproducible image from a URL. We'll use the [Binder `requirements.txt` example](https://github.com/binder-examples/requirements), which installs a simple Python environment. Run the following command:

```bash
jupyter-repo2docker https://github.com/binder-examples/requirements
```

You'll see `repo2docker` take the following actions:

1. Inspect the repository for [configuration files](#config-files). It will detect the `requirements.txt` file in the repository.
2. Build a Docker image using the configuration files. In this case, the `requirements.txt` file will correspond to a Python environment.
3. Run the image to let you explore the repository interactively.

Click the link provided and you'll be taken to an interactive Jupyter Notebook interface where you can run commands interactively inside the environment.

## Learn more

This is a simple example building an environment image for your repository.
To learn more about the kinds of source repositories, environments, and use-cases that repo2docker supports, see [the `repo2docker` user guide](./use/index.md).
