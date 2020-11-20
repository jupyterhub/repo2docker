# Architecture

This is a living document talking about the architecture of repo2docker
from various perspectives.

```eval_rst
.. _buildpacks:
```

## Buildpacks

The **buildpack** concept comes from [Heroku](https://devcenter.heroku.com/articles/buildpacks)
and Ruby on Rails' [Convention over Configuration](http://rubyonrails.org/doctrine/#convention-over-configuration)
doctrine.

Instead of the user specifying a complete specification of exactly how they want
their environment to be, they can focus only on how their environment differs from a conventional
environment. This means instead of deciding 'should I get Python from Apt or pyenv or ?', user
can just specify 'I want python-3.6'. Usually, specifying a **runtime** and list of **libraries**
with explicit **versions** is all that is needed.

In repo2docker, a Buildpack does the following things:

1. **Detect** if it can handle a given repository
2. **Build** a base language environment in the docker image
3. **Copy** the contents of the repository into the docker image
4. **Assemble** a specific environment in the docker image based on repository contents
5. **Push** the built docker image to a specific docker registry (optional)
6. **Run** the build docker image as a docker container (optional)

### Detect

When given a repository, repo2docker first has to determine which buildpack to use.
It takes the following steps to determine this:

1. Look at the ordered list of `BuildPack` objects listed in `Repo2Docker.buildpacks`
   traitlet. This is populated with a default set of buildpacks in most-specific-to-least-specific
   order. Other applications using this can add / change this using traditional
   [traitlet](http://traitlets.readthedocs.io/en/stable/) configuration mechanisms.
2. Calls the `detect` method of each `BuildPack` object. This method assumes that the repository
   is present in the current working directory, and should return `True` if the repository is
   something that it should be used for. For example, a `BuildPack` that uses `conda` to install
   libraries can check for presence of an `environment.yml` file and say 'yes, I can handle this
   repository' by returning `True`. Usually buildpacks look for presence of specific files
   (`requirements.txt`, `environment.yml`, `install.R`, `manifest.xml` etc) to determine if they can handle a
   repository or not. Buildpacks may also look into specific files to determine specifics of the
   required environment.
   More than one buildpack may use such information,
   as properties can be inherited.
3. If no `BuildPack` returns true, then repo2docker will use the default `BuildPack` (defined in
   `Repo2Docker.default_buildpack` traitlet).

### Build base environment

Once a buildpack is chosen, it builds a **base environment** that is mostly the same for various
repositories built with the same buildpack.

For example, in `CondaBuildPack`, the base environment consists of installing [miniconda](https://conda.io/miniconda.html)
and basic notebook packages (from `repo2docker/buildpacks/conda/environment.yml`). This is going
to be the same for most repositories built with `CondaBuildPack`, so we want to use
[docker layer caching](https://thenewstack.io/understanding-the-docker-cache-for-faster-builds/) as
much as possible for performance reasons. Next time a repository is built with `CondaBuildPack`,
we can skip straight to the **copy** step (since the base environment docker image *layers* have
already been built and cached).

The `get_build_scripts` and `get_build_script_files` methods are primarily used for this.
`get_build_scripts` can return arbitrary bash script lines that can be run as different users,
and `get_build_script_files` is used to copy specific scripts (such as a conda installer) into
the image to be run as pat of `get_build_scripts`. Code in either has following constraints:

1. You can *not* use the contents of repository in them, since this happens before the repository
   is copied into the image. For example, `pip install -r requirements.txt` will not work,
   since there's no `requirements.txt` inside the image at this point. This is an explicit
   design decision, to enable better layer caching.
2. You *may*, however, read the contents of the repository and modify the scripts emitted based
   on that! For example, in `CondaBuildPack`, if there's Python 2 specified in `environment.yml`,
   a different kind of environment is set up. The reading of the `environment.yml` is performed
   in the BuildPack itself, and not in the scripts returned by `get_build_scripts`. This is fine.
   BuildPack authors should still try to minimize the variants created in this fashion, to
   optimize the build cache.

### Copy repository contents

The contents of the repository are copied unconditionally into the Docker image, and made
available for all further commands. This is common to most `BuildPack`s, and the code is in
the `build` method of the `BuildPack` base class.

### Assemble repository environment

The **assemble** stage builds the specific environment that is requested by the repository.
This usually means installing required libraries specified in a format native to the language
(`requirements.txt`, `environment.yml`, `REQUIRE`, `install.R`, etc).

Most of this work is done in `get_assemble_scripts` method. It can return arbitrary bash script
lines that can be run as different users, and has access to the repository contents (unlike
`get_build_scripts`). The docker image layers produced by this usually can not be cached,
so less restrictions apply to this than to `get_build_scripts`.

At the end of the assemble step, the docker image is ready to be used in various ways!

### Push

Optionally, repo2docker can **push** a built image to a [docker registry](https://docs.docker.com/registry/).
This is done as a convenience only (since you can do the same with a `docker push` after using repo2docker
only to build), and implemented in `Repo2Docker.push` method. It is only activated if using the
`--push` commandline flag.

### Run

Optionally, repo2docker can **run** the built image and allow the user to access the Jupyter Notebook
running inside by default. This is also done as a convenience only (since you can do the same with `docker run`
after using repo2docker only to build), and implemented in `Repo2Docker.run`. It is activated by default
unless the `--no-run` commandline flag is passed.

## ContentProviders

ContentProviders provide a way for `repo2docker` to know how to find and
retrieve a repository. They follow a similar pattern as the BuildPacks
described above. When `repo2docker` is called, its main argument will be
a path to a repository. This might be a local path or a URL. Upon being called,
`repo2docker` will loop through all ContentProviders and perform the following
commands:

* Run the `detect()` method on the repository path given to `repo2docker`. This
  should return any value other than `None` if the path matches what the ContentProvider is looking
  for.

  > For example, the [`Local` ContentProvider](https://github.com/jupyterhub/repo2docker/blob/80b979f8580ddef184d2ba7d354e7a833cfa38a4/repo2docker/contentproviders/base.py#L64)
  > checks whether the argument is a valid local path. If so, then `detect(`
  > returns a dictionary: `{'path': source}` which defines the path to the repository.
  > This path is used by `fetch()` to check that it matches the output directory.
* If `detect()` returns something other than `None`, run `fetch()` with the
  returned value as its argument. This should
  result in the contents of the repository being placed locally to a folder.

For more information on ContentProviders, take a look at
[the ContentProvider base class](https://github.com/jupyterhub/repo2docker/blob/80b979f8580ddef184d2ba7d354e7a833cfa38a4/repo2docker/contentproviders/base.py#L16-L60)
which has more explanation.


