# Local Development

To develop & test repo2docker locally, you need:

1. Familiarity with using a command line terminal
2. A computer running macOS / Linux
3. Some knowledge of git
4. At least python 3.4
5. Your favorite text editor
6. A recent version of [Docker Community Edition](https://www.docker.com/community-edition)

## Clone the repository

First, you need to get a copy of the repo2docker git repository on your local
disk.

```bash
git clone https://github.com/jupyter/repo2docker
```

This will clone repo2docker into a directory called `repo2docker`. You can
make that your current directory with `cd repo2docker`.

## Set up local virtual environment

After cloning the repository (or your fork of the repo), you should set up an
isolated environment to install libraries required for running / developing
repo2docker. There are many ways to do this, and a `virtual environment` is
one of them.

```bash
python3 -m venv .
source bin/activate
pip3 install -e .
pip3 install -r dev-requirements.txt
```

This should install all the libraries required for testing & running repo2docker!

## Verify that docker is installed and running

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
subdirectory. These use [py.test](https://docs.pytest.org/).

You can run all the tests with:

```bash
py.test -s tests/*
```

If you want to run a specific test, you can do so with:

```bash
py.test -s tests/<path-to-test>
```

# Updating libraries installed for all repos

For both the `conda` and `virtualenv` (`pip`) base environments, we install specific
pinned versions of all dependencies. We explicitly list the dependencies
we want, then *freeze* them at commit time to explicitly list all the
transitive dependencies at current versions. This way, we know that
all dependencies will have the exact same version installed at all times.

To update one of the dependencies shared across all `repo2docker` builds, you
must follow these steps (with more detailed information in the sections below):

* Make sure you have [Docker](https://www.docker.com/) running on your computer
* Bump the version number in `virtualenv` ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#virtualenv-dependencies))
* Bump the version number in the `conda` environment ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#conda-dependencies))
* Make a pull request with your changes ([link](https://github.com/jupyter/repo2docker/blob/master/CONTRIBUTING.md#make-a-pull-request))

See the subsections below for more detailed instructions.

## Virtualenv dependencies

There are two files related to virtualenv dependencies:

1. `repo2docker/buildpacks/python/requirements.txt`

   Contains list of packages to install in Python3 virtualenvs,
   which are the default. **This where all Notebook versions &
   notebook extensions (such as JupyterLab / nteract) go**.

2. `repo2docker/buildpacks/python/requirements2.txt`

   Contains list of packages to install in Python2 virtualenvs, which
   can be specifically requested by users. **This only needs `IPyKernel`
   and kernel related libraries** - Notebook / Notebook Extension need
   not be installed here.

After you edit either of these files to add a new package / bump version on
an existing package, run `./repo2docker/buildpacks/python/freeze.bash`.

This script will resolve dependencies and write them to the respective `.frozen.txt`
files. You will need Python3 and Python2 with virtualenv to run the script.

All the `.txt` files in `repo2docker/buildpacks/python/` should be committed to git.

## Conda dependencies

There are two files related to conda dependencies:

1. `repo2docker/buildpacks/conda/environment.yml`

   Contains list of packages to install in Python3 conda environments,
   which are the default. **This is where all Notebook versions &
   notebook extensions (such as JupyterLab / nteract) go**.

2. `repo2docker/buildpacks/conda/environment.py-2.7.yml`

   Contains list of packages to install in Python2 conda environments, which
   can be specifically requested by users. **This only needs `IPyKernel`
   and kernel related libraries** - Notebook / Notebook Extension need
   not be installed here.

Once you edit either of these files to add a new package / bump version on
an existing package, you should then run `./repo2docker/buildpacks/conda/freeze.py`.
This script will resolve dependencies and write them to the respective `.frozen.yml`
files. You will need `docker` installed to run this script.

After the freeze script finishes, a number of files will have been created.
Commit the following subset of files to git:

```
repo2docker/buildpacks/conda/environment.yml
repo2docker/buildpacks/conda/environment.frozen.yml
repo2docker/buildpacks/conda/environment.py-2.7.yml
repo2docker/buildpacks/conda/environment.py-2.7.frozen.yml
repo2docker/buildpacks/conda/environment.py-3.5.frozen.yml
repo2docker/buildpacks/conda/environment.py-3.6.frozen.yml
```


## Make a Pull Request

Once you've made the commit, please make a Pull Request to the `jupyter/repo2docker`
repository, with a description of what versions were bumped / what new packages were
added and why.

# Release Process

We try to make a release of repo2docker every few months if possible.

## Access

To release repo2docker, you will need proper access credentials prior to beginning the process.

1. Access to the PyPI package for repo2docker
2. Access to push tags to the jupyter/repo2docker repository
3. Acess to push images to dockerhub on jupyter/repo2docker

If you do not have access to any of these, please contact a current maintainer of the project!

## Steps

1. Make a PR bumping version number of repo2docker in the
   `setup.py` file (like https://github.com/jupyter/repo2docker/pull/221),
   get it merged, and make sure your local checkout is the
   same as `master` on GitHub.

2. In your environment, install packages needed to make releases:
   ```bash
   pip install wheel twine
   ```

3. Clean out the `dist` directory and then build the `wheel` and `tar.gz` files:
   ```bash
   rm -f dist/*
   python setup.py sdist bdist_wheel
   ```
4. Once tests pass, time to upload!
   ```bash
   twine upload dist/*
   ```

   This might ask for your PyPI username and password.

5. Make a git tag and push it to GitHub:
   ```bash
   git tag -a v<version>
   git push official --tags
   ```

6. Tag and push a docker image:
   ```bash
   docker build -t jupyter/repo2docker:v<version> .
   docker push jupyter/repo2docker:v<version>
   ```
