# Overview of tests for the conda buildpack

## Tested configuration files

- [`.binder/`](https://repo2docker.readthedocs.io/en/latest/usage.html#where-to-put-configuration-files)
- [`requirements.txt`](https://repo2docker.readthedocs.io/en/latest/config_files.html#requirements-txt-install-a-python-environment)
- [`postBuild](https://repo2docker.readthedocs.io/en/latest/config_files.html#postbuild-run-code-after-installing-the-environment)

## Tested repo2docker command line flags

- [`--target-repo-dir`](https://repo2docker.readthedocs.io/en/latest/usage.html#cmdoption-jupyter-repo2docker-target-repo-dir)

### py2

- Test setup of a Python 2 environment by declaring `python=2` in
  `environment.yml`.

### py35-binder-dir

- Test setup of a Python 3.5 environment by declaring `python=3.5` in
  `environment.yml`.

  The reasons for testing 3.5 specifically is that it is the oldest version of
  Python 3 supported by repo2docker's conda buildpack. See
  `repo2docker/buildpacks/conda` for details.

- Test use of a `.binder` directory.

### py310-requirements-file

- Test setup of a Python 3.10 environment by declaring `python=3.10` in
  `environment.yml`.

  The reasons for testing 3.10 specifically is that it is the newest version of
  Python 3 supported by repo2docker's conda buildpack. See
  `repo2docker/buildpacks/conda` for details.

- Test use of a `requirements.txt` file, where an `environment.yml` file should
  take precedence and the `requirements.txt` should be ignored.

### py-r-postbuild-file

- Test setup of the default Python environment by omitting `python` from
  `environment.yml` file.

- Test setup of the default R environment by specifying `r-base` in
  `environment.yml`.

- Test use of a `postBuild` file.

### r3.6-target-repo-dir-flag

- Test setup of a R 3.6 environment by specifying `r-base=3.6` in
  `environment.yml`.

- Test use of repo2docker with the `--target-repo-dir` flag.

  `--target-repo-dir` is meant to support custom paths where repositories can be
  copied to besides `${HOME}`.
  
  This test makes use of the `test-extra-args.yaml` file to influence additional
  arguments passed to `repo2docker` during the test. In this test, specify
  `--target-repo-dir=/srv/repo`.
