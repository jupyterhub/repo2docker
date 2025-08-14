# Command-line usage and API

`repo2docker` is called with this command:

```
repo2docker <source-repository>
```

where `<source-repository>` is a repository in one of [the supported repository providers](#repository-providers).

For example, the following command will build an image of Peter Norvig's
[Pytudes] repository:

```
repo2docker https://github.com/norvig/pytudes
```

Building the image may take a few minutes.

[Pytudes] uses a [`requirements.txt` file](https://github.com/norvig/pytudes/blob/HEAD/requirements.txt) to specify its Python environment. Because of this, `repo2docker` will use `pip` to install dependencies listed in this `requirements.txt` file, and these will be present in the generated Docker image. To learn more about configuration files in `repo2docker` visit [](#config-files).

When the image is built, a message will be output to your terminal:

```
Copy/paste this URL into your browser when you connect for the first time,
to login with a token:
    http://0.0.0.0:36511/?token=f94f8fabb92e22f5bfab116c382b4707fc2cade56ad1ace0
```

Pasting the URL into your browser will open Jupyter Notebook with the
dependencies and contents of the source repository in the built image.

## Debug repo2docker with `--debug` and `--no-build`

To debug the container image being built, pass the `--debug` parameter:

> ```bash
> repo2docker --debug https://github.com/norvig/pytudes
> ```

This will print the generated `Dockerfile`, build it, and run it.

To see the generated `Dockerfile` without actually building it, pass `--no-build` to the commandline.
This `Dockerfile` output is for **debugging purposes** of `repo2docker` only - it can not be used by Docker directly.

> ```bash
> repo2docker --no-build --debug https://github.com/norvig/pytudes
> ```

## Build from a branch, commit or tag

To build a particular branch and commit, use the argument `--ref` and
specify the `branch-name` or `commit-hash`. For example:

```
repo2docker --ref 9ced85dd9a84859d0767369e58f33912a214a3cf https://github.com/norvig/pytudes
```

:::{tip}
For reproducible builds, we recommend specifying a commit-hash to
deterministically build a fixed version of a repository. Not specifying a
commit-hash will result in the latest commit of the repository being built.
:::

## Set environment variables during builds

When running repo2docker locally you can use the `-e` or `--env` command-line
flag for each variable that you want to define.

For example:

```bash
repo2docker -e VAR1=val1 -e VAR2=val2 ...
```

You can also configure environment variables for all users of a repository using the
[](#config-start) configuration file.

(command-line-api)=

## Command-line API

```{autoprogram} repo2docker.__main__:argparser
:prog: repo2docker
```

[pytudes]: https://github.com/norvig/pytudes
