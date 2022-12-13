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
