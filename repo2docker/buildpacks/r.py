import datetime
import os
import re
from functools import lru_cache

import requests

from ..semver import parse_version as V
from ._r_base import rstudio_base_scripts
from .python import PythonBuildPack

# Aproximately the first snapshot on RSPM (Posit package manager)
# that seems to have a working IRKernel.
RSPM_CUTOFF_DATE = datetime.date(2018, 12, 7)


class RBuildPack(PythonBuildPack):
    """
    Setup R for use with a repository

    This sets up R + RStudio + IRKernel for a repository that contains:

    1. A `runtime.txt` file with the text:

       r-<year>-<month>-<date>

       Where 'year', 'month' and 'date' refer to a specific
       date whose CRAN snapshot we will use to fetch packages.
       Uses https://packagemanager.posit.co.

    2. A `DESCRIPTION` file signaling an R package

    If there is no `runtime.txt`, then the CRAN snapshot is set to latest
    date that is guaranteed to exist across timezones.

    Additional R packages are installed if specified either

    - in a file `install.R`, that will be executed at build time,
      and can be used for installing packages from both CRAN and GitHub

    - as dependencies in a `DESCRIPTION` file

    - are needed by a specific tool

    R is installed from https://docs.rstudio.com/resources/install-r/
    """

    @property
    def runtime(self):
        """
        Return contents of runtime.txt if it exists, '' otherwise
        """
        if not hasattr(self, "_runtime"):
            runtime_path = self.binder_path("runtime.txt")
            try:
                with open(runtime_path) as f:
                    self._runtime = f.read().strip()
            except FileNotFoundError:
                self._runtime = ""

        return self._runtime

    @property
    def r_version(self):
        """Detect the R version for a given `runtime.txt`

        Will return the version specified by the user or the current default
        version.
        """
        # Available versions at https://cran.r-project.org/src/base/
        version_map = {
            "4.2": "4.2.1",
            "4.1": "4.1.3",
            "4.0": "4.0.5",
            "3.6": "3.6.3",
            "3.5": "3.5.3",
            "3.4": "3.4.4",
            "3.3": "3.3.3",
        }

        # the default if nothing is specified
        # Use full version is needed here, so it a valid semver
        #
        # NOTE: When updating this version, also update
        #       - tests/unit/test_r.py -> test_version_specification
        #       - tests/r/r-rspm-apt/verify
        #
        r_version = version_map["4.2"]

        if not hasattr(self, "_r_version"):
            parts = self.runtime.split("-")
            # If runtime.txt is not set, or if it isn't of the form r-<version>-<yyyy>-<mm>-<dd>,
            # we don't use any of it in determining r version and just use the default
            if len(parts) == 5:
                r_version = parts[1]
                # For versions of form x.y, we want to explicitly provide x.y.z - latest patchlevel
                # available. Users can however explicitly specify the full version to get something specific
                if r_version in version_map:
                    r_version = version_map[r_version]

            # translate to the full version string
            self._r_version = r_version

        return self._r_version

    @property
    def checkpoint_date(self):
        """
        Return the date of CRAN checkpoint to use for this repo

        Returns '' if no date is specified
        """
        if not hasattr(self, "_checkpoint_date"):
            match = re.match(r"r-(\d.\d(.\d)?-)?(\d\d\d\d)-(\d\d)-(\d\d)", self.runtime)
            if not match:
                self._checkpoint_date = False
            else:
                # turn the last three groups of the match into a date
                self._checkpoint_date = datetime.date(
                    *[int(s) for s in match.groups()[-3:]]
                )

        return self._checkpoint_date

    def detect(self):
        """
        Check if current repo should be built with the R Build pack

        super().detect() is not called in this function - it would return
        false unless a `requirements.txt` is present and we do not want
        to require the presence of a `requirements.txt` to use R.
        """
        # If no date is found, then self.checkpoint_date will be False
        # Otherwise, it'll be a date object, which will evaluate to True
        if self.checkpoint_date:
            return True

        description_R = "DESCRIPTION"
        if not self.binder_dir and os.path.exists(description_R):
            if not self.checkpoint_date:
                # no R snapshot date set through runtime.txt
                # Set it to two days ago from today
                self._checkpoint_date = datetime.date.today() - datetime.timedelta(
                    days=2
                )
                self._runtime = f"r-{str(self._checkpoint_date)}"
            return True

    @lru_cache()
    def get_env(self):
        """
        Set custom env vars needed for RStudio to load
        """
        return super().get_env() + [
            # rstudio (rsession) can't seem to find R unless we explicitly tell it where
            # it is - just $PATH isn't enough. I discovered these are the env vars it
            # looks for by digging through RStudio source and finding
            # https://github.com/rstudio/rstudio/blob/v2022.02.3+492/src/cpp/r/session/RDiscovery.cpp
            ("R_HOME", f"/opt/R/{self.r_version}/lib/R"),
            ("R_DOC_DIR", "${R_HOME}/doc"),
            ("LD_LIBRARY_PATH", "${R_HOME}/lib:${LD_LIBRARY_PATH}"),
        ]

    @lru_cache()
    def get_path(self):
        """
        Return paths to be added to the PATH environment variable.

        The RStudio package installs its binaries in a non-standard path,
        so we explicitly add that path to PATH.
        """
        return super().get_path() + ["/usr/lib/rstudio-server/bin/"]

    @lru_cache()
    def get_build_env(self):
        """
        Return environment variables to be set.

        We want libraries to be installed in a path that users can write to
        without needing root. This is set via the `R_LIBS_USER` environment
        variable, so we set that here.
        """
        return super().get_build_env() + [
            # This is the path where user libraries are installed
            ("R_LIBS_USER", "${APP_BASE}/rlibs")
        ]

    @lru_cache()
    def get_packages(self):
        """
        Return list of packages to be installed.

        We install a base version of R, and packages required for RStudio to
        be installed.
        """
        packages = [
            # For rstudio
            "psmisc",
            "libapparmor1",
            "sudo",
            "lsb-release",
            "libssl-dev",
        ]

        return super().get_packages().union(packages)

    @lru_cache()
    def get_rspm_snapshot_url(self, snapshot_date, max_days_prior=7):
        for i in range(max_days_prior):
            snapshots = requests.post(
                "https://packagemanager.posit.co/__api__/url",
                # Ask for midnight UTC snapshot
                json={
                    "repo": "all",
                    "snapshot": (snapshot_date - datetime.timedelta(days=i)).strftime(
                        "%Y-%m-%dT00:00:00Z"
                    ),
                },
            ).json()
            # Construct a snapshot URL that will give us binary packages for appropriate ubuntu version
            if "upsi" in snapshots:
                return (
                    # Env variables here are expanded by envsubst in the Dockerfile, after sourcing
                    # /etc/os-release. This allows us to use distro specific variables here to get
                    # appropriate binary packages without having to hard code version names here.
                    "https://packagemanager.posit.co/all/__linux__/${VERSION_CODENAME}/"
                    + snapshots["upsi"]
                )
        raise ValueError(
            "No snapshot found for {} or {} days prior in packagemanager.posit.co".format(
                snapshot_date.strftime("%Y-%m-%d"), max_days_prior
            )
        )

    @lru_cache()
    def get_devtools_snapshot_url(self):
        """
        Return url of snapshot to use for getting devtools install

        devtools is part of our 'core' base install, so we should have some
        control over what version we install here.
        """
        # Picked from https://packagemanager.posit.co/client/#/repos/1/overview
        # Hardcoded rather than dynamically determined from a date to avoid extra API calls
        # Plus, we can always use packagemanager.posit.co here as we always install the
        # necessary apt packages.
        # Env variables here are expanded by envsubst in the Dockerfile, after sourcing
        # /etc/os-release. This allows us to use distro specific variables here to get
        # appropriate binary packages without having to hard code version names here.
        return "https://packagemanager.posit.co/all/__linux__/${VERSION_CODENAME}/2022-06-03+Y3JhbiwyOjQ1MjYyMTU7RkM5ODcwN0M"

    @lru_cache()
    def get_build_scripts(self):
        """
        Return series of build-steps common to all R repositories

        All scripts here should be independent of contents of the repository.

        This sets up:

        - A directory owned by non-root in ${R_LIBS_USER}
          for installing R packages into
        - RStudio
        - R's devtools package, at a particular frozen version
          (determined by CRAN)
        - IRKernel
        - nbrsessionproxy (to access RStudio via Jupyter Notebook)

        We set the snapshot date used to install R libraries from based on the
        contents of runtime.txt.
        """
        if self.checkpoint_date < RSPM_CUTOFF_DATE:
            raise RuntimeError(
                f'Microsoft killed MRAN, the source of R package snapshots before {RSPM_CUTOFF_DATE.strftime("%Y-%m-%d")}. '
                f'This repo has a snapshot date of {self.checkpoint_date.strftime("%Y-%m-%d")} specified in runtime.txt. '
                "Please use a newer snapshot date"
            )

        cran_mirror_url = self.get_rspm_snapshot_url(self.checkpoint_date)

        if self.platform != "linux/amd64":
            raise RuntimeError(
                f"RStudio is only available for linux/amd64 ({self.platform})"
            )
        scripts = [
            (
                "root",
                rf"""
                apt-get update > /dev/null && \
                apt-get install --yes --no-install-recommends \
                        libclang-dev \
                        libzmq3-dev > /dev/null && \
                wget --quiet -O /tmp/r-{self.r_version}.deb \
                    https://cdn.rstudio.com/r/ubuntu-$(. /etc/os-release && echo $VERSION_ID | sed 's/\.//')/pkgs/r-{self.r_version}_1_amd64.deb && \
                apt install --yes --no-install-recommends /tmp/r-{self.r_version}.deb > /dev/null && \
                rm /tmp/r-{self.r_version}.deb && \
                apt-get -qq purge && \
                apt-get -qq clean && \
                rm -rf /var/lib/apt/lists/* && \
                ln -s /opt/R/{self.r_version}/bin/R /usr/local/bin/R && \
                ln -s /opt/R/{self.r_version}/bin/Rscript /usr/local/bin/Rscript && \
                R --version
                """,
            ),
        ]

        scripts += rstudio_base_scripts(self.r_version)

        scripts += [
            (
                "root",
                r"""
                mkdir -p ${R_LIBS_USER} && \
                chown -R ${NB_USER}:${NB_USER} ${R_LIBS_USER}
                """,
            ),
            (
                "root",
                # Set paths so that RStudio shares libraries with base R
                # install. This first comments out any R_LIBS_USER that
                # might be set in /etc/R/Renviron and then sets it.
                rf"""
                sed -i -e '/^R_LIBS_USER=/s/^/#/' /opt/R/{self.r_version}/lib/R/etc/Renviron && \
                echo "R_LIBS_USER=${{R_LIBS_USER}}" >> /opt/R/{self.r_version}/lib/R/etc/Renviron
                """,
            ),
            (
                "root",
                # RStudio's CRAN mirror needs this to figure out which binary package to serve.
                # If not set properly, it will just serve up source packages
                # Quite hilarious, IMO.
                # See https://docs.rstudio.com/rspm/1.0.12/admin/binaries.html
                # Set mirror for RStudio too, by modifying rsession.conf
                rf"""
                R RHOME && \
                mkdir -p /etc/rstudio && \
                EXPANDED_CRAN_MIRROR_URL="$(. /etc/os-release && echo {cran_mirror_url} | envsubst)" && \
                echo "options(repos = c(CRAN = \"${{EXPANDED_CRAN_MIRROR_URL}}\"))" > /opt/R/{self.r_version}/lib/R/etc/Rprofile.site && \
                echo "r-cran-repos=${{EXPANDED_CRAN_MIRROR_URL}}" > /etc/rstudio/rsession.conf
                """,
            ),
            (
                "root",
                # Configure log-level and send to stderr
                # Set log-level=debug to investigate problems
                # https://docs.posit.co/ide/server-pro/server_management/logging.html
                rf"""
                printf '[*]\nlog-level=info\nlogger-type=stderr\n' > /etc/rstudio/logging.conf
                """,
            ),
            (
                "${NB_USER}",
                # Install a pinned version of devtools, IRKernel and shiny
                rf"""
                export EXPANDED_CRAN_MIRROR_URL="$(. /etc/os-release && echo {cran_mirror_url} | envsubst)" && \
                R --quiet -e "install.packages(c('devtools', 'IRkernel', 'shiny'), repos=Sys.getenv(\"EXPANDED_CRAN_MIRROR_URL\"))" && \
                R --quiet -e "IRkernel::installspec(prefix=Sys.getenv(\"NB_PYTHON_PREFIX\"))"
                """,
            ),
        ]

        return super().get_build_scripts() + scripts

    @lru_cache()
    def get_preassemble_script_files(self):
        files = super().get_preassemble_script_files()
        installR_path = self.binder_path("install.R")
        if os.path.exists(installR_path):
            files[installR_path] = installR_path

        return files

    @lru_cache()
    def get_preassemble_scripts(self):
        """Install contents of install.R

        Attempt to execute `install.R` before copying the contents of the
        repository. We speculate that most of the time we do not need access.
        In case this fails we re-run it after copying the repository contents.

        The advantage of executing it before copying is that minor edits to the
        repository content will not trigger a re-install making things faster.
        """
        scripts = []

        installR_path = self.binder_path("install.R")
        if os.path.exists(installR_path):
            scripts += [
                (
                    "${NB_USER}",
                    # Delete /tmp/downloaded_packages only if install.R fails, as the second
                    # invocation of install.R might be able to reuse them
                    f"Rscript {installR_path} && touch /tmp/.preassembled || true && rm -rf /tmp/downloaded_packages",
                )
            ]

        return super().get_preassemble_scripts() + scripts

    @lru_cache()
    def get_assemble_scripts(self):
        """Install the dependencies of or the repository itself"""
        assemble_scripts = super().get_assemble_scripts()

        installR_path = self.binder_path("install.R")
        if os.path.exists(installR_path):
            assemble_scripts += [
                (
                    "${NB_USER}",
                    # only run install.R if the pre-assembly failed
                    # Delete any downloaded packages in /tmp, as they aren't reused by R
                    f"""if [ ! -f /tmp/.preassembled ]; then Rscript {installR_path}; rm -rf /tmp/downloaded_packages; fi""",
                )
            ]

        description_R = "DESCRIPTION"
        if not self.binder_dir and os.path.exists(description_R):
            assemble_scripts += [
                ("${NB_USER}", 'R --quiet -e "devtools::install_local(getwd())"')
            ]

        return assemble_scripts
