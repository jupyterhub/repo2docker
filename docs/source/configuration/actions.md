# Configuration files for post-build actions

(postbuild)=

## `postBuild` - Run code after installing the environment

A script that can contain arbitrary commands to be run after the whole repository has been built. If you
want this to be a shell script, make sure the first line is `#!/bin/bash`.

Note that by default the build will not be stopped if an error occurs inside a shell script.
You should include `set -e` or the equivalent at the start of the script to avoid errors being silently ignored.

An example use-case of `postBuild` file is JupyterLab's demo on mybinder.org.
It uses a `postBuild` file in a folder called `.binder` to [prepare
their demo for binder](https://github.com/jupyterlab/jupyterlab-demo/blob/HEAD/.binder/postBuild).

(start)=

## `start` - Run code before the user sessions starts

A script that can contain simple commands to be run at runtime (as an
[ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint)
to the docker container). If you want this to be a shell script, make sure the
first line is `#!/bin/bash`. The last line must be `exec "$@"`
or equivalent.

Use this to set environment variables that software installed in your container
expects to be set. This script is executed each time your binder is started and
should at most take a few seconds to run.

If you only need to run things once during the build phase use {ref}`postBuild`.

% TODO: Discuss runtime limits, best practices, etc.
