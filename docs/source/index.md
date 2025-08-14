# Welcome to `repo2docker`'s documentation

`repo2docker` lets you **reproducibly build, run, and deploy user environment images for interactive computing and data workflows from source code repositories**.

`repo2docker` can be used to explore a repository locally by building and executing the
constructed image of the repository, or as a means of building images that
are pushed to a Docker registry. It is the tool used by [BinderHub](https://binderhub.readthedocs.io) to build images on demand.

::::{grid}
:::{grid-item-card} 🔧 Build reproducible data science environments from repositories
Build a reproducible data science environment as a Docker image and execute code interactively. Use many [configuration files](#config-files) to control language, tools, and setup instructions.
:::
:::{grid-item-card} 🚀 Deploy environments in JupyterHub or Binder
Push environment images to a Docker registry for re-use in data science environment services like [JupyterHub](https://jupyterhub.readthedocs.io) or [a Binder instance](https://mybinder.org), or for other communities to build upon your base environment.
:::
:::{grid-item-card} ☁️ Host repositories in many providers
Host repositories in a provider like GitHub, an open science repository like [Zenodo](https://zenodo.org) or [Figshare](https://figshare.com), a hosted data platform like a [Dataverse installation](https://dataverse.org/), an archive like the
[Software Heritage Archive](https://archive.softwareheritage.org).
:::
::::

## What is a user image and why would I build one with `repo2docker`?

A **user image** contains the entire software environment that a user may access from an interactive data science session. For example, it might contain many **programming languages**, **software for data analysis**, or even **content files and datasets** available to anybody that accesses that environment. User images are built with [Docker](https://www.docker.com/), a standard open source tool for defining, building, and deploying images.

Many data science platforms and services like [JupyterHub](https://jupyterhub.readthedocs.io) and [Binder](https://mybinder.org) launch interactive data science sessions **with a user image attached**, meaning that the user gains access to whatever is in the image. In short, this allows somebody to define and build the user image one time, in a way that users can reproducibly re-use many times.

Dockerfiles are the standard way that Docker images are defined[^use-dockerfile].
However, **building images with Dockerfiles takes expertise and time** that is outside the scope of a data scientist or researcher. `repo2docker` makes this workflow more accessible by using community-standard configuration files for computational reproducibility to build user images.

In short, `repo2docker` is a tool to reproducibly build, run, and deploy these user environment Docker images for data science from source code repositories.

[^use-dockerfile]: That said, you can still use a Dockerfile if you really want to!

## How `repo2docker` works

When you call `repo2docker` like so:

```
repo2docker <source-repository>
```

It performs these steps:

1. Inspects the repository for [configuration files](#config-files). These will be used to build the environment needed to run the repository.
2. Builds a Docker image with an environment specified in these [configuration files](#config-files).
3. Runs the image to let you explore the repository interactively via Jupyter notebooks, RStudio, or many other interfaces (this is optional).
4. Pushes the images to a Docker registry so that it may be accessed remotely (this is optional).

[swhid]: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html

Please report [Bugs](https://github.com/jupyterhub/repo2docker/issues),
[ask questions](https://gitter.im/jupyterhub/binder) or
[contribute to the project](https://github.com/jupyterhub/repo2docker/blob/HEAD/CONTRIBUTING.md).

## Get started with repo2docker

This tutorial walks you through setting up repo2docker, building your first environment image, and running it locally with Docker.

```{toctree}
:maxdepth: 2

start
```

## Learn how to use repo2docker

Our user guide provides all of the information you need to configure and deploy the environment image you want.

```{toctree}
:maxdepth: 2
use/index
```

## Contribute to repo2docker

Our contributor guide describes how you can follow along with the project, learn how to collaborate with our open team, and learn developer workflows and information.

```{toctree}
:maxdepth: 2

contribute/index
```

```{toctree}
:caption: Changelog
:maxdepth: 2
:hidden: true

changelog
```
