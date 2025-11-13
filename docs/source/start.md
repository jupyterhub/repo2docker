# Get started

This tutorial guides you through installing `repo2docker` and building your first environment image.

## Prerequisite

### Python

`repo2docker` requires Python 3.6 or above.

### Container Engine

`repo2docker` requires a container engine compatible with the specification published by the [Open Container Initiative](https://opencontainers.org/).

#### Docker

```{important}
Only the [Docker Engine](https://docs.docker.com/engine/) is open source. [Docker Desktop](https://docs.docker.com/get-started/get-docker/) requires a license.
```

Follow [Docker's official installation steps](https://docs.docker.com/get-started/get-docker/).

#### Podman

Follow [Podman's official installation steps](https://podman.io/docs/installation).

After completing the installation of Podman,

1. create a [listening service for Podman](https://docs.podman.io/en/latest/markdown/podman-system-service.1.html) by running

   ```bash
   systemctl --user start podman.socket
   ```

1. configure the `DOCKER_HOST` environment variable following [Podman's official procedure](https://podman-desktop.io/docs/migrating-from-docker/using-the-docker_host-environment-variable#procedure). You might want to configure the `DOCKER_HOST` environment variable to persist in your `~/.bashrc`.

(install)=

## Install `repo2docker`

### Install `repo2docker` with `pip`

It is recommend to install `repo2docker` with the `pip` tool:

```bash
python3 -m pip install jupyter-repo2docker
```

(usage)=

## Build a repository with `repo2docker`

Now that you've installed a container engine and `repo2docker`, you can build a repository.
To do so, continue following this guide.

### Start the container engine

Ensure that the container engine is running.

#### Docker

Follow the [offcial instructions for starting Docker](https://docs.docker.com/engine/daemon/start/).

#### Podman

Run

```bash
podman info
```

### Build an image from a URL

Next we'll build a reproducible image from a URL. We'll use the [Binder `requirements.txt` example](https://github.com/binder-examples/requirements), which installs a simple Python environment. Run the following command:

```bash
jupyter-repo2docker https://github.com/binder-examples/requirements
```

You'll see `repo2docker` take the following actions:

1. Inspect the repository for [configuration files](#config-files). It will detect the `requirements.txt` file in the repository.
2. Build a container image using the configuration files. In this case, the `requirements.txt` file will correspond to a Python environment.
3. Run the image to let you explore the repository interactively.

Click the link provided and you'll be taken to an interactive Jupyter Notebook interface where you can run commands interactively inside the environment.

## Learn more

This is a simple example building an environment image for your repository.
To learn more about the kinds of source repositories, environments, and use-cases that `repo2docker` supports, see [the `repo2docker` user guide](./use/index.md).
