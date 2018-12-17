# Contributing to repo2docker development

## Process for making a code contribution

This outlines the process for getting changes to the code of
repo2docker merged.

* If your change is relatively significant, **open an issue to discuss**
  before spending a lot of time writing code. Getting consensus with the
  community is a great way to save time later.
* Make edits in your fork of the repo2docker repository
* Submit a pull request (this is how all changes are made)
* Edit [the changelog](./../../changelog.html)
  by appending your feature / bug fix to the development version.
* Wait for a community member to merge your changes
* (optional) Deploy a new version of repo2docker to mybinder.org by [following these steps](http://mybinder-sre.readthedocs.io/en/latest/deployment/how.html)


## Guidelines to getting a Pull Request merged

These are not hard rules to be enforced by 🚓 but instead guidelines
to help you make a contribution.

* prefix the title of your pull request with `[MRG]` if the contribution
  is complete and should be subjected to a detailed review;
* create a PR as early as possible, marking it with `[WIP]` while you work on
  it (good to avoid duplicated work, get broad review of functionality or API,
  or seek collaborators);
* a PR solves one problem (do not mix problems together in one PR) with the
  minimal set of changes;
* describe why you are proposing the changes you are proposing;
* try to not rush changes (the definition of rush depends on how big your
  changes are);
* Enter your changes into the [change log](https://github.com/jupyter/repo2docker/blob/master/CHANGES.rst);
* someone else has to merge your PR;
* new code needs to come with a test;
* apply [PEP8](https://www.python.org/dev/peps/pep-0008/) as much
  as possible, but not too much;
* no merging if travis is red;
* do use merge commits instead of merge-by-squashing/-rebasing. This makes it
  easier to find all changes since the last deployment `git log --merges --pretty=format:"%h %<(10,trunc)%an %<(15)%ar %s" <deployed-revision>..`


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
disk. Fork the repository on GitHub, then clone it to your computer:

```bash
git clone https://github.com/<your-username>/repo2docker
```

This will clone repo2docker into a directory called `repo2docker`. You can
make that your current directory with `cd repo2docker`.

### Set up a local virtual environment

After cloning the repository (or your fork of the repository), you should set up an
isolated environment to install libraries required for running / developing
repo2docker.

There are many ways to do this but here we present you with two approaches: `virtual environment` or `pipenv`.

- Using `virtual environment`

```bash
python3 -m venv .
source bin/activate
pip3 install -e .
pip3 install -r dev-requirements.txt
pip3 install -r docs/doc-requirements.txt
```

This should install all the libraries required for testing & running repo2docker!

- Using `pipenv`

Note that you will need to install pipenv first using `pip3 install pipenv`.
Then from the root directory of this project you can use the following commands:

```bash
pipenv install --dev
```

This should install both the dev and docs requirements at once!

### Set up

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
