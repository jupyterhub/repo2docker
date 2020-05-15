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
2. Bump the version numbers of the dependencies you want to update in the `conda` environment ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#conda-dependencies))
3. Make a pull request with your changes ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#make-a-pull-request))

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

We try to make a release of repo2docker every few months if possible.

We follow [semantic versioning](https://semver.org/).

A new release will automatically be created when a new git tag is created
and pushed to the repository (using
[Travis CI](https://github.com/jupyter/repo2docker/blob/master/.travis.yml#L52)).

To create a new release, follow these steps:

### Confirm that the changelog is ready

[The changelog](https://github.com/jupyter/repo2docker/blob/master/docs/source/changelog.rst)
should reflect all significant enhancements and fixes to repo2docker and
its documentation. In addition, ensure that the correct version is displayed
at the top, and create a new `dev` section if needed.

### Create a new tag and push it

First, tag a new release locally:

```bash
V=0.7.0; git tag -am "release $V" $V
```

Then push this change up to the master repository

```
git push origin --tags
```

Travis should automatically run the tests and, if they pass, create a
new release on the [repo2docker PyPI](https://pypi.org/project/jupyter-repo2docker/).
Once this has completed, make sure that the new version has been updated.

### Create a new release on the GitHub repository

Once the new release has been pushed to PyPI, we need to create a new
release on the [GitHub repository releases page](https://github.com/jupyter/repo2docker/releases). Once on that page, follow these steps:

* Click "Draft a new release"
* Choose a tag version using the same tag you just created above
* The release name is simply the tag version
* The description is [a link to the Changelog](https://github.com/jupyter/repo2docker/blob/master/docs/source/changelog.rst),
  ideally with an anchor to the latest release.
* Finally, click "Publish release"

That's it!

## Update the change log

To add your change to the change log, find the relevant Feature/Bug
fix/API change section for the next release near the top of the file;
then add one or two sentences as a new bullet point about your
changes. Include the pull request or issue number between square
brackets at the end.

Some details:

- versioning follows the x.y.z, major.minor.bugfix numbering

- bug fixes go into the next bugfix release. If there isn't any, you
  can create a new section (see point below). Don't worry if you're
  not sure about that, and think it should go into a next major or
  minor release: an admin will let you know, or move the change later
  to the appropriate section

- API changes should preferably go into the next major release, unless
  they are backward compatible (for example, a deprecated function
  keyword): then they can go into the next minor release. For release
  with major release 0, non-backward compatible breaking changes are
  also fine for the next minor release.

- new features should go into the next minor release.

- if there is no section for the appropriate release, you can add one:

  follow the versioning scheme, by simply increasing the relevant
  number for one of the major /minor/bugfix numbers, appropriate for
  your change (see the above bullet points); add the release
  section. Then add three subsections: new features, api changes, and
  bug fixes. Leave out the sections that are not appropriate for the
  newlye added release section.

Release candidate versions in the change log are only temporary, and
should be superseded by either a next release candidate, or the final
release for that version (bugfix version 0).


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
    docker run --rm -t -v "$(pwd)":"$(pwd)" --user 1000 jupyter/repo2docker:"$1" jupyter-repo2docker --no-build --debug "$(pwd)" &> "$basename"."$1"
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
