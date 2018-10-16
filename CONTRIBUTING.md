# Contributing to repo2docker development

This document covers:

- Process for making a code contribution
- Setting up for Local Development
- Running Tests
- Updating and Freezing BuildPack Dependencies
- Updating the change log
- Creating a Release


## Process for making a code contribution

This outlines the process for getting changes to the code of
repo2docker merged. This serves as information on when a PR is "done".

Contributions should follow these guidelines:

* all changes by pull request (PR);
* please prefix the title of your pull request with `[MRG]` if the contribution
  is complete and should be subjected to a detailed review;
* create a PR as early as possible, marking it with `[WIP]` while you work on
  it (good to avoid duplicated work, get broad review of functionality or API,
  or seek collaborators);
* a PR solves one problem (do not mix problems together in one PR) with the
  minimal set of changes;
* describe why you are proposing the changes you are proposing;
* try to not rush changes (the definition of rush depends on how big your
  changes are);
* someone else has to merge your PR;
* new code needs to come with a test;
* apply [PEP8](https://www.python.org/dev/peps/pep-0008/) as much
  as possible, but not too much;
* no merging if travis is red;
* do use merge commits instead of merge-by-squashing/-rebasing. This makes it
  easier to find all changes since the last deployment `git log --merges --pretty=format:"%h %<(10,trunc)%an %<(15)%ar %s" <deployed-revision>..`
* [when you merge do deploy to mybinder.org](http://mybinder-sre.readthedocs.io/en/latest/deployment/how.html)

These are not hard rules to be enforced by :police_car: but instead guidelines.


## Setting up for Local Development

To develop & test repo2docker locally, you need:

1. Familiarity with using a command line terminal
2. A computer running macOS / Linux
3. Some knowledge of git
4. At least python 3.6
5. Your favorite text editor
6. A recent version of [Docker Community Edition](https://www.docker.com/community-edition)

### Clone the repository

First, you need to get a copy of the repo2docker git repository on your local
disk.

```bash
git clone https://github.com/jupyter/repo2docker
```

This will clone repo2docker into a directory called `repo2docker`. You can
make that your current directory with `cd repo2docker`.

### Set up a local virtual environment

After cloning the repository (or your fork of the repository), you should set up an
isolated environment to install libraries required for running / developing
repo2docker. There are many ways to do this, and a `virtual environment` is
one of them.

```bash
python3 -m venv .
source bin/activate
pip3 install -e .
pip3 install -r dev-requirements.txt
pip3 install -r docs/doc-requirements.txt
```

This should install all the libraries required for testing & running repo2docker!

### Verify that docker is installed and running

If you do not already have [Docker](https://www.docker.com/), you should be able
to download and install it for your operating system using the links from the
[official website](https://www.docker.com/community-edition). After you have
installed it, you can verify that it is working by running the following commands:

```bash
docker version
```

It should output something like:

```
Client:
 Version:      17.09.0-ce
 API version:  1.32
 Go version:   go1.8.3
 Git commit:   afdb6d4
 Built:        Tue Sep 26 22:42:45 2017
 OS/Arch:      linux/amd64

Server:
 Version:      17.09.0-ce
 API version:  1.32 (minimum version 1.12)
 Go version:   go1.8.3
 Git commit:   afdb6d4
 Built:        Tue Sep 26 22:41:24 2017
 OS/Arch:      linux/amd64
 Experimental: false
```

Then you are good to go!


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

### Updating libraries installed for all repositories

For both the `conda` and `virtualenv` (`pip`) base environments in the **Conda BuildPack** and **Python BuildPack**,
we install specific pinned versions of all dependencies. We explicitly list the dependencies
we want, then *freeze* them at commit time to explicitly list all the
transitive dependencies at current versions. This way, we know that
all dependencies will have the exact same version installed at all times.

To update one of the dependencies shared across all `repo2docker` builds, you
must follow these steps (with more detailed information in the sections below):

* Make sure you have [Docker](https://www.docker.com/) running on your computer
* Bump the version numbers of the dependencies you want to update in the `conda` environment ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#conda-dependencies))
* Make a pull request with your changes ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#make-a-pull-request))

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


### Change log

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


### Make a Pull Request

Once you've made the commit, please make a Pull Request to the `jupyterhub/repo2docker`
repository, with a description of what versions were bumped / what new packages were
added and why. If you fix a bug or add new functionality consider adding a new
test to prevent the bug from coming back/the feature breaking in the future.


## Creating a Release

We try to make a release of repo2docker every few months if possible.

We follow semantic versioning.

Check hat the Change log is ready and then tag a new release on GitHub.

When the travis run completes check that the new release is available on PyPI.
