# Using source repositories

(usage-config-file-location)=

## Where to put configuration files in a repository

`repo2docker` will look for configuration files in the following order:

- The root directory of the repository.
- A folder named `binder/` or `.binder/` in the root of the repository.

  If one of these folders exists, only configuration files in that folder are considered, configuration in the root directory will be ignored.
  Having both `binder/` and `.binder/` folders is not allowed.

Check the complete list of [configuration files](#config-files) supported
by `repo2docker` to see how to configure the build process.

(repository-providers)=

## Supported repository providers

repo2docker can fetch repositories from a number of repositories. Here are the ones we support:

- A URL of a Git repository (`https://github.com/binder-examples/requirements`),
- A Zenodo DOI (`10.5281/zenodo.1211089`),
- A [SWHID] (`swh:1:rev:999dd06c7f679a2714dfe5199bdca09522a29649`),
- A URL of a [CKAN] dataset (`https://demo.ckan.org/dataset/sample-dataset-1`)
- A path to a local directory (`a/local/directory`)

[swhid]: https://docs.softwareheritage.org/devel/swh-model/persistent-identifiers.html
[ckan]: https://ckan.org

In each case you can build from these repository sources like so:

```bash
jupyter-repo2docker <URL-ID-or-path>
```

## Supported version control systems

These Version Control Systems are supported by `repo2docker`.

### Git

Any `git` repository is supported with `repo2docker`.
These are generally stored in [a git repository provider](#repository-providers) like [GitHub](https://github.com).

### Mercurial

For [Mercurial](https://www.mercurial-scm.org) repositories, Mercurial and
[hg-evolve](https://www.mercurial-scm.org/doc/evolution/) need to be
installed. For example, on Debian based distributions, one can do:

```
sudo apt install mercurial
$(hg debuginstall --template "{pythonexe}") -m pip install hg-evolve --user
```

To install Mercurial on other systems, see [here](https://www.mercurial-scm.org/download).

Note that for old Mercurial versions, you may need to specify a version for
hg-evolve. For example, `hg-evolve==9.2` for hg 4.5 (which is installed with
`apt` on Ubuntu 18.4).
