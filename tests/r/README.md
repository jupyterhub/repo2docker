# Overview of tests for the R buildpack

## Tested configuration files

- [`runtime.txt`](https://repo2docker.readthedocs.io/en/latest/config_files.html#runtime-txt-specifying-runtimes).
- [`DESCRIPTION`](https://repo2docker.readthedocs.io/en/latest/config_files.html#description-install-an-r-package).
- [`install.R`](https://repo2docker.readthedocs.io/en/latest/config_files.html#install-r-install-an-r-rstudio-environment).
- [`requirements.txt`](https://repo2docker.readthedocs.io/en/latest/config_files.html#requirements-txt-install-a-python-environment)
- [`apt.txt`](https://repo2docker.readthedocs.io/en/latest/config_files.html#apt-txt-install-packages-with-apt-get)

## Test folders

### r-rspm-apt-file

- Test setup of the default R environment by omitting a version specification in
  `runtime.txt`, where the date provided in `runtime.txt` is recent enough for a
  RSPM snapshot of CRAN to be used.

- Test use of a `apt.txt` file.

### r-rspm-description-file

- Test use of a `DESCRIPTION` file instead of an `install.R` file, where a
  `runtime.txt` is omitted and a recent enough snapshot date is assumed a RSPM
  snapshot of CRAN to be used.

### r4.0-rspm

- Test setup of a R 4.0 environment by specifying `r-4.0-...` in `runtime.txt`,
  where the date provided in `runtime.txt` is recent enough for a RSPM snapshot
  of CRAN to be used.
