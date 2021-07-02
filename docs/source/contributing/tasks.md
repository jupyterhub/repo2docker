# Common tasks

These are some common tasks to be done as a part of developing
and maintaining repo2docker. If you'd like more guidance for how
to do these things, reach out in the [JupyterHub Gitter channel](https://gitter.im/jupyterhub/jupyterhub).

## Running tests

We have a lot of tests for various cases supported by repo2docker in the `tests/`
subdirectory. If you fix a bug or add new functionality consider adding a new
test to prevent the bug from coming back. These use
[py.test](https://docs.pytest.org/).

You can run all the tests with:

```bash
py.test -s tests/*
```

If you want to run a specific test, you can do so with:

```bash
py.test -s tests/<path-to-test>
```

To skip the tests related to Mercurial repositories (to avoid to install
Mercurial and hg-evolve), one can use the environment variable
``REPO2DOCKER_SKIP_HG_TESTS``.

### Troubleshooting Tests

Some of the tests have non-python requirements for your development machine. They are:

- `git-lfs` must be installed ([instructions](https://github.com/git-lfs/git-lfs)). It need not be activated -- there is no need to run the `git lfs install` command. It just needs to be available to the test suite.
   - If your test failure messages include "`git-lfs filter-process: git-lfs: command not found`", this step should address the problem.

- Minimum Docker Image size of 128GB is required. If you are not running docker on a linux OS, you may need to expand the runtime image size for your installation. See Docker's instructions for [macOS](https://docs.docker.com/docker-for-mac/space/) or [Windows 10](https://docs.docker.com/docker-for-windows/#resources) for more information.
    - If your test failure messages include "`No space left on device: '/home/...`", this step should address the problem.

## Update and Freeze BuildPack Dependencies

This section covers the process by which repo2docker defines and updates the
dependencies that are installed by default for several buildpacks.

For both the `conda` and `virtualenv` (`pip`) base environments in the **Conda BuildPack** and **Python BuildPack**,
we install specific pinned versions of all dependencies. We explicitly list the dependencies
we want, then *freeze* them at commit time to explicitly list all the
transitive dependencies at current versions. This way, we know that
all dependencies will have the exact same version installed at all times.

To update one of the dependencies shared across all `repo2docker` builds, you
must follow these steps (with more detailed information in the sections below):

1. Make sure you have [Docker](https://www.docker.com/) running on your computer
2. Bump the version numbers of the dependencies you want to update in the `conda` environment ([link](https://github.com/jupyterhub/repo2docker/blob/master/CONTRIBUTING.md#conda-dependencies))
3. Make a pull request with your changes ([link](https://github.com/jupyterhub/repo2docker/blob/master/CONTRIBUTING.md#make-a-pull-request))

See the subsections below for more detailed instructions.


### Conda dependencies

1. There are two files related to conda dependencies. Edit as needed.

    - `repo2docker/buildpacks/conda/environment.yml`

       Contains list of packages to install in Python3 conda environments,
       which are the default. **This is where all Notebook versions &
       notebook extensions (such as JupyterLab / nteract) go**.

    - `repo2docker/buildpacks/conda/environment.py-2.7.yml`

       Contains list of packages to install in Python2 conda environments, which
       can be specifically requested by users. **This only needs `IPyKernel`
       and kernel related libraries**. Notebook / Notebook Extension need
       not be installed here.

2. Once you edit either of these files to add a new package / bump version on
   an existing package, you should then run:

   ```bash
   cd ./repo2docker/buildpacks/conda/
   python freeze.py
   ```

   This script will resolve dependencies and write them to the respective `.frozen.yml`
   files. You will need `docker` installed to run this script.

3. After the freeze script finishes, a number of files will have been created.
   Commit the following subset of files to git:

    ```
    repo2docker/buildpacks/conda/environment.yml
    repo2docker/buildpacks/conda/environment.frozen.yml
    repo2docker/buildpacks/conda/environment.py-2.7.yml
    repo2docker/buildpacks/conda/environment.py-2.7.frozen.yml
    repo2docker/buildpacks/conda/environment.py-3.5.frozen.yml
    repo2docker/buildpacks/conda/environment.py-3.6.frozen.yml
    ```

5. Make a pull request; see details below.

6. Once the pull request is approved (but not yet merged), Update the
   change log (details below) and commit the change log, then update
   the pull request.


### Make a Pull Request

Once you've made the commit, please make a Pull Request to the `jupyterhub/repo2docker`
repository, with a description of what versions were bumped / what new packages were
added and why. If you fix a bug or add new functionality consider adding a new
test to prevent the bug from coming back/the feature breaking in the future.


## Creating a Release

We make a release of whatever is on `master` every month. We use "calendar versioning".
Monthly releases give users a predictable pattern for when releases are going to
happen and prevents locking up improvements for fixes for long periods of time.

A new release will automatically be created when a new git tag is created
and pushed to the repository.

To create a new release, follow these steps:

### Create a new tag and push it

First, tag a new release locally:

```bash
V=YYYY.MM.0; git tag -am "release $V" $V
```

> If you need to make a second (or third) release in a month increment the
> trailing 0 of the version to 1 (or 2).

Then push this change up to the master repository

```
git push origin --tags
```

GitHub Actions should create a
new release on the [repo2docker PyPI](https://pypi.org/project/jupyter-repo2docker/).
Once this has completed, make sure that the new version has been updated.

### Create a new release on the GitHub repository

Once the new release has been pushed to PyPI, we need to create a new
release on the [GitHub repository releases page](https://github.com/jupyterhub/repo2docker/releases). Once on that page, follow these steps:

* Click "Draft a new release"
* Choose a tag version using the same tag you just created above
* The release name is simply the tag version
* Finally, click "Publish release"

That's it!


## Keeping the Pipfile and requirements files up to date

We now have both a `dev-requirements.txt` and a `Pifile` for repo2docker, as
such it is important to keep these in sync/up-to-date.

Both files use `pip identifiers` so if you are updating for example the Sphinx version
in the `doc-requirements.txt` (currently `Sphinx = ">=1.4,!=1.5.4"`) you can use the
same syntax to update the Pipfile and viceversa.

At the moment this has to be done manually so please make sure to update both
files accordingly.

# Uncommon tasks

## Compare generated Dockerfiles between repo2docker versions

For larger refactorings it can be useful to check that the generated Dockerfiles match
between an older version of r2d and the current version. The following shell script
automates this test.

```bash
#! /bin/bash -e

current_version=$(jupyter-repo2docker --version | sed s@+@-@)
echo "Comparing $(pwd) (local $current_version vs. $R2D_COMPARE_TO)"
basename="dockerfilediff"

diff_r2d_dockerfiles_with_version () {
    docker run --rm -t -v "$(pwd)":"$(pwd)" --user 1000 jupyterhub/repo2docker:"$1" jupyter-repo2docker --no-build --debug "$(pwd)" &> "$basename"."$1"
    jupyter-repo2docker --no-build --debug "$(pwd)" &> "$basename"."$current_version"

    # remove first line logging the path
    sed -i '/^\[Repo2Docker\]/d' "$basename"."$1"
    sed -i '/^\[Repo2Docker\]/d' "$basename"."$current_version"

    diff --strip-trailing-cr "$basename"."$1" "$basename"."$current_version" | colordiff
    rm "$basename"."$current_version" "$basename"."$1"
}

startdir="$(pwd)"
cd "$1"

#diff_r2d_dockerfiles 0.10.0-22.g4f428c3.dirty
diff_r2d_dockerfiles_with_version "$R2D_COMPARE_TO"

cd "$startdir"
```

Put the code above in a file `tests/dockerfile_diff.sh` and make it executable: `chmod +x dockerfile_diff.sh`.

Configure the repo2docker version you want to compare with your local version in the environment variable `R2D_COMPARE_TO`.
The scripts takes one input: the directory where repo2docker should be executed.

```bash
cd tests/
R2D_COMPARE_TO=0.10.0 ./dockerfile_diff.sh venv/py35/
```

Run it for all directories where there is a `verify` file:

```bash
cd tests/
R2D_COMPARE_TO=0.10.0 CMD=$(pwd)/dockerfile_diff.sh find . -name 'verify' -execdir bash -c '$CMD $(pwd)' \;
```

To keep the created Dockefilers for further inspection, comment out the deletion line in the script.
