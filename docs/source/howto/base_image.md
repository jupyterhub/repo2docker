# Change the base image used by Docker

You may change the base image used in the `Dockerfile` that creates images by repo2docker.
This is equivalent to changing the `FROM <base_image>` in the Dockerfile.

To do so, use the `base_image` traitlet when invoking `repo2docker`.
Note that this is not configurable by individual repositories, it is configured when you invoke the `repo2docker` command.

```{note}
By default repo2docker builds on top of the `buildpack-deps:bionic` base image, an Ubuntu-based image.
```

## Requirements for your base image

`repo2docker` will only work if a specific set of packages exists in the base image.
Only images that match the following criteria are supported:

- Ubuntu based distributions (minimum `18.04`)
- Contains a set of base packages installed with [the `buildpack-deps` image family](https://hub.docker.com/_/buildpack-deps).

Other images _may_ work, but are not officially supported.

## This will affect reproducibility 🚨

Changing the base image may have an impact on the reproducibility of repositories that are built.
There are **no guarantees that repositories will behave the same way as other repo2docker builds if you change the base image**.
For example these are two scenarios that would make your repositories non-reproducible:

- **Your base image is different from `Ubuntu:bionic`.**
  If you change the base image in a way that is different from repo2docker's default (the Ubuntu `bionic` image), then repositories that **you** build with repo2docker may be significantly different from those that **other** instances of repo2docker build (e.g., those from [`mybinder.org`](https://mybinder.org)).
- **Your base image changes over time.**
  If you choose a base image that changes its composition over time (e.g., an image provided by some other community), then it may cause repositories build with your base image to change in unpredictable ways.
  We recommend choosing a base image that you know to be stable and trustworthy.
