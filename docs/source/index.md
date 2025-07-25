# Welcome to `repo2docker`'s documentation

`repo2docker` lets you **build, run, and push Docker images for data science from source code repositories**.

`repo2docker` can be used to explore a repository locally by building and executing the
constructed image of the repository, or as a means of building images that
are pushed to a Docker registry.

`repo2docker` can build a reproducible computational environment for any repository that
follows the [Reproducible Executable Environment Specification](./specification.md). Repositories can be pulled from a number of repository providers, such as the URL of a Git repository, a [DOI](https://en.wikipedia.org/wiki/Digital_object_identifier) from Zenodo or Figshare, a [Handle](https://en.wikipedia.org/wiki/Handle_System) or DOI from a Dataverse installation, a [SWHID] of a directory of a revision archived in the
[Software Heritage Archive](https://archive.softwareheritage.org), or a path to a local directory.

`repo2docker` is the tool used by [BinderHub](https://binderhub.readthedocs.io)
to build images on demand.

## How `repo2docker` works

When you call `repo2docker` like so:

```
jupyter-repo2docker <URL of repository>
```

It performs these steps:

1. Inspects the repository for [configuration files](#config-files). These will be used to build the environment needed to run the repository.
2. Builds a Docker image with an environment specified in these [configuration files](#config-files).
3. Runs the image to let you explore the repository interactively via Jupyter notebooks, RStudio, or many other interfaces (this is optional)
4. Pushes the images to a Docker registry so that it may be accessed remotely (this is optional)

[swhid]: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html

Please report [Bugs](https://github.com/jupyterhub/repo2docker/issues),
[ask questions](https://gitter.im/jupyterhub/binder) or
[contribute to the project](https://github.com/jupyterhub/repo2docker/blob/HEAD/CONTRIBUTING.md).

## Get started with repo2docker

This tutorial walks you setting up repo2docker, building your first environment image, and running it locally with Docker.

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

Our contirbutor guide describes how you can follow along with the project, learn how to collaborate with our open team, and learn developer workflows and information.

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
