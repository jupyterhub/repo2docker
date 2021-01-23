# Contributing to repo2docker

Thank you for thinking about contributing to repo2docker!
This is an open source project that is developed and maintained entirely by volunteers.
*Your contribution* is integral to the future of the project.
THANK YOU!

## Types of contribution

There are many ways to contribute to repo2docker:

* **Update the documentation.**
  If you're reading a page or docstring and it doesn't make sense (or doesn't exist!), please let us know by opening a bug report.
  It's even more amazing if you can give us a suggested change.
* **Fix bugs or add requested features.**
  Have a look through the [issue tracker](https://github.com/jupyterhub/repo2docker/issues) and see if there are any tagged as ["help wanted"](https://github.com/jupyterhub/repo2docker/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22).
  As the label suggests, we'd love your help!
* **Report a bug.**
  If repo2docker isn't doing what you thought it would do then open a [bug report](https://github.com/jupyterhub/repo2docker/issues/new?template=bug_report.md).
  That issue template will ask you a few questions described in more detail below.
* **Suggest a new feature.**
  We know that there are lots of ways to extend repo2docker!
  If you're interested in adding a feature then please open a [feature request](https://github.com/jupyterhub/repo2docker/issues/new?template=feature_request.md).
  That issue template will ask you a few questions described in detail below.
* **Review someone's Pull Request.**
  Whenever somebody proposes changes to the repo2docker codebase, the community reviews
  the changes, and provides feedback, edits, and suggestions. Check out the
  [open pull requests](https://github.com/jupyterhub/repo2docker/pulls?q=is%3Apr+is%3Aopen+sort%3Aupdated-desc)
  and provide feedback that helps improve the PR and get it merged. Please keep your
  feedback positive and constructive!
* **Tell people about repo2docker.**
  As we said above, repo2docker is built by and for its community.
  If you know anyone who would like to use repo2docker, please tell them about the project!
  You could give a talk about it, or run a demonstration.
  The sky is the limit :rocket::star2:.

If you're not sure where to get started, then please come and say hello in our [Gitter channel](https://gitter.im/jupyterhub/binder), or open an discussion thread at the [Jupyter discourse forum](https://discourse.jupyter.org/).

## Process for making a contribution

This outlines the process for getting changes to the repo2docker project merged.

1. Identify the correct issue template: [bug report](https://github.com/jupyterhub/repo2docker/issues/new?template=bug_report.md) or [feature request](https://github.com/jupyterhub/repo2docker/issues/new?template=feature_request.md).

    **Bug reports** ([examples](https://github.com/jupyterhub/repo2docker/issues?q=is%3Aissue+is%3Aopen+label%3Abug), [new issue](https://github.com/jupyterhub/repo2docker/issues/new?template=bug_report.md)) will ask you for a description of the problem, the expected behaviour, the actual behaviour, how to reproduce the problem, and your personal set up.
    Bugs can include problems with the documentation, or code not running as expected.

    It is really important that you make it easy for the maintainers to reproduce the problem you're having.
    This guide on creating a [minimal, complete and verifiable example](https://stackoverflow.com/help/mcve) is a great place to start.

    **Feature requests** ([examples](https://github.com/jupyterhub/repo2docker/labels/needs%3A%20discussion), [new issue](https://github.com/jupyterhub/repo2docker/issues/new?template=feature_request.md)) will ask you for the proposed change, any alternatives that you have considered, a description of who would use this feature, and a best-guess of how much work it will take and what skills are required to accomplish.

    Very easy feature requests might be updates to the documentation to clarify steps for new users.
    Harder feature requests may be to add new functionality to the project and will need more in depth discussion about who can complete and maintain the work.

    Feature requests are a great opportunity for you to advocate for the use case you're suggesting.
    They help others understand how much effort it would be to integrate the work,and - if you're successful at convincing them that this effort is worth it - make it more likely that they to choose to work on it with you.

2. Open an issue.
  Getting consensus with the community is a great way to save time later.
3. Make edits in [your fork](https://help.github.com/en/articles/fork-a-repo) of the [repo2docker repository](https://github.com/jupyterhub/repo2docker).
4. Make a [pull request](https://help.github.com/en/articles/about-pull-requests).
Read the [next section](#guidelines-to-getting-a-pull-request-merged) for guidelines for both reviewers and contributors on merging a PR.
6. Wait for a community member to merge your changes.
  Remember that **someone else must merge your pull request**.
  That goes for new contributors and long term maintainers alike.
  Because `master` is continuously deployed to mybinder.org it is essential
  that `master` is always in a deployable state.
7. (optional) Deploy a new version of repo2docker to mybinder.org by [following these steps](http://mybinder-sre.readthedocs.io/en/latest/deployment/how.html)

## Guidelines to getting a Pull Request merged

These are not hard rules to be enforced by 🚓 but they are suggestions written by the repo2docker maintainers to help complete your contribution as smoothly as possible for both you and for them.

* **Create a PR as early as possible**, marking it with `[WIP]` while you work on it.
  This avoids duplicated work, lets you get high level feedback on functionality or API changes, and/or helps find collaborators to work with you.
* **Keep your PR focused.**
  The best PRs solve one problem.
  If you end up changing multiple things, please open separate PRs for the different conceptual changes.
* **Add tests to your code.**
  PRs will not be merged if Travis is failing.
* **Apply [PEP8](https://www.python.org/dev/peps/pep-0008/)** as much as possible, but not too much.
  If in doubt, ask.
* **Use merge commits** instead of merge-by-squashing/-rebasing.
  This makes it easier to find all changes since the last deployment `git log --merges --pretty=format:"%h %<(10,trunc)%an %<(15)%ar %s" <deployed-revision>..` and your PR easier to review.
* **Make it clear when your PR is ready for review.**
  Prefix the title of your pull request (PR) with `[MRG]` if the contribution is complete and should be subjected to a detailed review.
* **Use commit messages to describe _why_ you are proposing the changes you are proposing.**
* **Try to not rush changes** (the definition of rush depends on how big your changes are).
  Remember that everyone in the repo2docker team is a volunteer and we can not (nor would we want to) control their time or interests.
  Wait patiently for a reviewer to merge the PR.
  (Remember that **someone else** must merge your PR, even if you have the admin rights to do so.)

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

After cloning the repository, you should set up an
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
pip3 install black
```

This should install all the libraries required for testing & running repo2docker!

- Using `pipenv`

Note that you will need to install pipenv first using `pip3 install pipenv`.
Then from the root directory of this project you can use the following commands:

```bash
pipenv install --dev
```

This should install both the dev and docs requirements at once!


### Code formatting

We use [`black`](https://black.readthedocs.io/en/stable/) as code formatter to
get a consistent layout for all the code in this project. This makes reading
the code easier.

To format your code run `black .` in the top-level directory of this repository.
Many editors have plugins that will automatically apply black as you edit files.

We also have a pre-commit hook setup that will check that code is formatted
according to black's style guide. You can activate it with `pre-commit install`.

As part of our continuous integration tests we will check that code is
formatted properly and the tests will fail if this is not the case.


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

## Building the documentation locally

If you only changed the documentation, you can also build the documentation locally using `sphinx` .

```bash
pip install -r docs/doc-requirements.txt

cd docs/
make html
```

Then open the file `docs/build/html/index.html` in your browser.
