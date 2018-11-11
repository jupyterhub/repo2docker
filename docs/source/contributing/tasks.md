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

We follow semantic versioning.

Check that the Change log is ready and then tag a new release on GitHub.

When the travis run completes check that the new release is available on PyPI.


### Update the change log

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
