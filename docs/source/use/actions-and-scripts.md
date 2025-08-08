# Run scripts, commands, and actions as part of environment building

In addition to installing using [standard configuration files](#config-files), you can run your own custom actions and commands as part of the build or user session launch process.

(commands-jovyan)=
## Commands are run as the `jovyan` user and not root

Whenever you run a custom command, it is run as a special user called `jovyan`.
It **does not have `root` privileges**.
So, you should choose actions that do not require these privileges.

For example, if you're using a `postBuild` script to install and use a new environment manager like [the `pixi` CLI](https://pixi.sh/latest/), make sure to install and configure it to a location accessible (and writable) to a user. For example:

- ✅ `$CONDA_BIN` would work, because `conda` puts its binary folder in a user-accessible space.
- ✅ `~/.local/bin` would work, because it's in the home directory.
- ❌ `/usr/bin` would *NOT* work, because it requires root privileges to write to.

## Run commands before finalizing your environment image

You can run arbitrary commands before finalizing your environment image.
This is useful in cases like:

- You want to install and use custom environment management software that isn't supported by [repo2docker's configuration files](#config-files) (e.g., `pixi`).
- You want to run custom commands to setup the environment properly (e.g., download a small dataset and put it in a specific location in the image).

To do so, use a `postBuild` script, see [](#postbuild) for more information.

## Run commands before launching a new user session

You can run commands before launching a new **user session**.
These are not baked into the environment image, they'll only be run once an image has been launched, but before the user's interactive session has been created.

This is useful for things like:

- Start a local server running that you want a user to have access to.
- Updating a local dataset that always needs to have the latest information in it.

To do so, use a `start` script. See [](#config-start) for more information.
