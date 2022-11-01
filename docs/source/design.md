# Design of repo2docker

The repo2docker buildpacks are inspired by
[Heroku's Build Packs](https://devcenter.heroku.com/articles/buildpacks).
The philosophy for the repo2docker buildpacks includes:

- using common configuration files for familiar installation and packaging tools
- allowing configuration files to be combined to compose more complex setups
- specifying default locations for configuration files
  (in the repository's root, `binder` or `.binder` directory)

When designing `repo2docker` and adding to it in the future, the
developers are influenced by two primary use cases.
The use cases for `repo2docker` which drive most design decisions are:

1. Automated image building used by projects like
   [BinderHub](http://github.com/jupyterhub/binderhub)
2. Manual image building and running the image from the command line client,
   `jupyter-repo2docker`, by users interactively on their workstations

## Deterministic output

The core of `repo2docker` can be considered a
[deterministic algorithm](https://en.wikipedia.org/wiki/Deterministic_algorithm).
When given an input directory which has a particular repository checked out, it
deterministically produces a Dockerfile based on the contents of the directory.
So if we run `repo2docker` on the same directory multiple times, we get the
exact same Dockerfile output.

This provides a few advantages:

1. Reuse of cached built artifacts based on a repository's identity increases
   efficiency and reliability. For example, if we had already run `repo2docker`
   on a git repository at a particular commit hash, we know we can just re-use
   the old output, since we know it is going to be the same. This provides
   massive performance & architectural advantages when building additional
   tools (like BinderHub) on top of `repo2docker`.
2. We produce Dockerfiles that have as much in common as possible across
   multiple repositories, enabling better use of the Docker build cache. This
   also provides massive performance advantages.

## Reproducibility and version stability

Many ingredients go into making an image from a repository:

1. version of the base docker image
1. version of `repo2docker` itself
1. versions of the libraries installed by the repository

`repo2docker` controls the first two, the user controls the third one. The current
policy for the version of the base image is that we will use the current LTS
version Bionic Beaver (18.04) for the foreseeable future.

The version of `repo2docker` used to build an image can influence which packages
are installed by default and which features are supported during the build
process. We will periodically update those packages to keep step with releases
of Jupyter Notebook, JupyterLab, etc. For packages that are installed by
default but where you want to control the version we recommend you specify them
explicitly in your dependencies.

## Unix principles "do one thing well"

`repo2docker` should do one thing, and do it well. This one thing is:

> Given a repository, deterministically build a docker image from
> it.

There's also some convenience code (to run the built image) for users, but
that's separated out cleanly. This allows easy use by other projects (like
BinderHub).

There is additional (and very useful) design advice on this in
the [Art of Unix Programming](https://web.archive.org/web/20190921131144/http://www.faqs.org/docs/artu/ch01s06.html) which
is a highly recommended quick read.

## Composability

Although other projects, like
[s2i](https://github.com/openshift/source-to-image), exist to convert source to
Docker images, `repo2docker` provides the additional functionality to support
_composable_ environments. We want to easily have an image with
Python3+Julia+R-3.2 environments, rather than just one single language
environment. While generally one language environment per container works well,
in many scientific / datascience computing environments you need multiple
languages working together to get anything done. So all buildpacks are
composable, and need to be able to work well with other languages.

## [Pareto principle](https://en.wikipedia.org/wiki/Pareto_principle) (The 80-20 Rule)

Roughly speaking, we want to support 80% of use cases, and provide an escape
hatch (raw Dockerfiles) for the other 20%. We explicitly want to provide support
only for the most common use cases - covering every possible use case never ends
well.

An easy process for getting support for more languages here is to demonstrate
their value with Dockerfiles that other people can use, and then show that this
pattern is popular enough to be included inside `repo2docker`. Remember that 'yes'
is forever (very hard to remove features!), but 'no' is only temporary!
