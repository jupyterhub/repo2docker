# Frequent tasks

These are some frequent tasks to be done as a part of developing
and maintaining repo2docker. If you'd like more guidance for how
to do these things, reach out in the [JupyterHub Gitter channel](https://gitter.im/jupyterhub/jupyterhub).

:::{admonition} Set up your development environment first!
:class: tip
Before attempting most tasks, follow the directions to [set up your development environment](contributing:local-dev).

Though note that many of these tasks do **not** require Docker.
:::

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
`REPO2DOCKER_SKIP_HG_TESTS`.

### Troubleshooting Tests

Some of the tests have non-python requirements for your development machine. They are:

- `git-lfs` must be installed ([instructions](https://github.com/git-lfs/git-lfs)). It need not be activated -- there is no need to run the `git lfs install` command. It just needs to be available to the test suite.
  - If your test failure messages include "`git-lfs filter-process: git-lfs: command not found`", this step should address the problem.

- Minimum Docker Image size of `128GB` is required. If you are not running Docker on a Linux OS, you may need to expand the runtime image size for your installation. See Docker's [instructions for macOS](https://docs.docker.com/docker-for-mac/space/) or [instructions for Windows 10](https://docs.docker.com/docker-for-windows/#resources) for more information.
  - If your test failure messages include "`No space left on device: '/home/...`", this step should address the problem.

## Update and Freeze BuildPack Dependencies

This section covers the process by which repo2docker defines and updates the
dependencies that are installed by default for several buildpacks.

For both the `conda` and `virtualenv` (`pip`) base environments in the **Conda BuildPack** and **Python BuildPack**,
we install specific pinned versions of all dependencies. We explicitly list the dependencies
we want, then _freeze_ them at commit time to explicitly list all the
transitive dependencies at current versions. This way, we know that
all dependencies will have the exact same version installed at all times.

To update one of the dependencies shared across all `repo2docker` builds, you
must follow these steps (with more detailed information in the sections below):

1. Bump the version numbers of the dependencies you want to update in the `conda` environment ([link](tasks:conda-dependencies))
2. Make a pull request with your changes ([link](https://github.com/jupyterhub/repo2docker/blob/HEAD/CONTRIBUTING.md#make-a-pull-request))

See the subsections below for more detailed instructions.

(tasks:conda-dependencies)=

### Conda dependencies

1. There are two files related to conda dependencies. Edit as needed.
   - `repo2docker/buildpacks/conda/environment.yml`

     Contains list of packages to install in Python3 conda environments,
     which are the default. **This is where all Notebook versions &
     notebook extensions (such as JupyterLab) go**.

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

   This script will resolve dependencies and write them to the respective `.lock`
   files.

3. After the freeze script finishes, a number of files will have been **modified**.
   They roughly follow this pattern:

   ```
   repo2docker/buildpacks/conda/environment*
   ```

   You should **commit all modified files** to git.

4. Make a Pull Request to the `jupyterhub/repo2docker` repository, with a description
   of what versions were bumped / what new packages were added and why. If you fix a
   bug or add new functionality consider adding a new test to prevent the bug from
   coming back/the feature breaking in the future.

5. Once the pull request is approved (but not yet merged), Update the
   change log (details below) and commit the change log, then update
   the pull request.

## Creating a Release

We encourage a release of whatever is on `main` every month. We use "[calendar versioning](https://calver.org/)".

A new release will automatically be created when a new git tag is created
and pushed to the repository. See [previous releases](https://github.com/jupyterhub/repo2docker/releases) for examples.

To create a new release, follow these steps:

- Add the output of `github-activity` between now and last release, to the changelog and open a PR with this content
  - E.g. the activity since the date of the last release: `github-activity jupyterhub/repo2docker -s 2025-08-01`
- Go to the [GitHub repository](https://github.com/jupyterhub/repo2docker)
- Click `Draft a new release`
- Click `Tag`
  - Type in a new tag like `YYYY.MM.N` (where `N` is the release number this month, usually it is `0`)
- Title: `<Month> <Year>` (E.g., `August 2025`)
- Body: Paste the `github-activity` output from the changelog
- Click `Publish release`

This will create a new release **and a new tag**.
The creation of the tag will trigger the `.github/workflows/release.yml` action to publish the latest repo2docker package to PyPI.

You can confirm the new package is released [in our PyPI page](https://pypi.org/project/jupyter-repo2docker/#history).
