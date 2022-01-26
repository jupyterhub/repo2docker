import re
import os
import datetime
import requests


from ..semver import parse_version as V
from .python import PythonBuildPack
from ._r_base import rstudio_base_scripts


class RBuildPack(PythonBuildPack):
    """
    Setup R for use with a repository

    This sets up R + RStudio + IRKernel for a repository that contains:

    1. A `runtime.txt` file with the text:

       r-<year>-<month>-<date>

       Where 'year', 'month' and 'date' refer to a specific
       date whose CRAN snapshot we will use to fetch packages.
       Uses https://packagemanager.rstudio.com, or MRAN if no snapshot
       is found on packagemanager.rstudio.com

    2. A `DESCRIPTION` file signaling an R package

    If there is no `runtime.txt`, then the CRAN snapshot is set to latest
    date that is guaranteed to exist across timezones.

    Additional R packages are installed if specified either

    - in a file `install.R`, that will be executed at build time,
      and can be used for installing packages from both CRAN and GitHub

    - as dependencies in a `DESCRIPTION` file

    - are needed by a specific tool

    The `r-base-core` package from Ubuntu or "Ubuntu packages for R"
    apt repositories is used to install R itself,
    rather than any of the methods from https://cran.r-project.org/.

    The `r-base-dev` package is installed as advised in RStudio instructions.
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
        version_map = {
            "3.4": "3.4",
            "3.5": "3.5.3-1bionic",
            "3.5.0": "3.5.0-1bionic",
            "3.5.1": "3.5.1-2bionic",
            "3.5.2": "3.5.2-1bionic",
            "3.5.3": "3.5.3-1bionic",
            "3.6": "3.6.3-1bionic",
            "3.6.0": "3.6.0-2bionic",
            "3.6.1": "3.6.1-3bionic",
            "4.0": "4.0.5-1.1804.0",
            "4.0.2": "4.0.2-1.1804.0",
            "4.1": "4.1.2-1.1804.0",
        }
        # the default if nothing is specified
        r_version = "4.1"

        if not hasattr(self, "_r_version"):
            parts = self.runtime.split("-")
            if len(parts) == 5:
                r_version = parts[1]
                if r_version not in version_map:
                    raise ValueError(
                        "Version '{}' of R is not supported.".format(r_version)
                    )

            # translate to the full version string
            self._r_version = version_map.get(r_version)

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
                self._runtime = "r-{}".format(str(self._checkpoint_date))
            return True

    def get_path(self):
        """
        Return paths to be added to the PATH environment variable.

        The RStudio package installs its binaries in a non-standard path,
        so we explicitly add that path to PATH.
        """
        return super().get_path() + ["/usr/lib/rstudio-server/bin/"]

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
        ]
        # For R 3.4 we use the default Ubuntu package, for other versions we
        # install from a different apt repository
        if V(self.r_version) < V("3.5"):
            packages.append("r-base")
            packages.append("r-base-dev")
            packages.append("libclang-dev")

        return super().get_packages().union(packages)

    def get_rspm_snapshot_url(self, snapshot_date, max_days_prior=7):
        for i in range(max_days_prior):
            snapshots = requests.post(
                "https://packagemanager.rstudio.com/__api__/url",
                # Ask for midnight UTC snapshot
                json={
                    "repo": "all",
                    "snapshot": (snapshot_date - datetime.timedelta(days=i)).strftime(
                        "%Y-%m-%dT00:00:00Z"
                    ),
                },
            ).json()
            # Construct a snapshot URL that will give us binary packages for Ubuntu Bionic (18.04)
            if "upsi" in snapshots:
                return (
                    "https://packagemanager.rstudio.com/all/__linux__/bionic/"
                    + snapshots["upsi"]
                )
        raise ValueError(
            "No snapshot found for {} or {} days prior in packagemanager.rstudio.com".format(
                snapshot_date.strftime("%Y-%m-%d"), max_days_prior
            )
        )

    def get_mran_snapshot_url(self, snapshot_date, max_days_prior=7):
        for i in range(max_days_prior):
            try_date = snapshot_date - datetime.timedelta(days=i)
            # Fall back to MRAN if packagemanager.rstudio.com doesn't have it
            url = "https://mran.microsoft.com/snapshot/{}".format(try_date.isoformat())
            r = requests.head(url)
            if r.ok:
                return url
        raise ValueError(
            "No snapshot found for {} or {} days prior in mran.microsoft.com".format(
                snapshot_date.strftime("%Y-%m-%d"), max_days_prior
            )
        )

    def get_cran_mirror_url(self, snapshot_date):
        # Date after which we will use rspm + binary packages instead of MRAN + source packages
        rspm_cutoff_date = datetime.date(2022, 1, 1)

        if snapshot_date >= rspm_cutoff_date or self.r_version >= V("4.1"):
            return self.get_rspm_snapshot_url(snapshot_date)
        else:
            return self.get_mran_snapshot_url(snapshot_date)

    def get_devtools_snapshot_url(self):
        """
        Return url of snapshot to use for getting devtools install

        devtools is part of our 'core' base install, so we should have some
        control over what version we install here.
        """
        # Picked from https://packagemanager.rstudio.com/client/#/repos/1/overview
        # Hardcoded rather than dynamically determined from a date to avoid extra API calls
        # Plus, we can always use packagemanager.rstudio.com here as we always install the
        # necessary apt packages.
        return "https://packagemanager.rstudio.com/all/__linux__/bionic/2022-01-04+Y3JhbiwyOjQ1MjYyMTU7NzlBRkJEMzg"

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

        cran_mirror_url = self.get_cran_mirror_url(self.checkpoint_date)

        # Determine which R apt repository should be enabled
        if V(self.r_version) >= V("3.5"):
            if V(self.r_version) >= V("4"):
                vs = "40"
            else:
                vs = "35"

        scripts = [
            (
                "root",
                rf"""
                echo "deb https://cloud.r-project.org/bin/linux/ubuntu bionic-cran{vs}/" > /etc/apt/sources.list.d/r-ubuntu.list
                """,
            ),
            # Dont use apt-key directly, as gpg does not always respect *_proxy vars. This increase the chances
            # of being able to reach it from behind a firewall
            (
                "root",
                r"""
                wget --quiet -O - 'https://keyserver.ubuntu.com/pks/lookup?op=get&search=0xe298a3a825c0d65dfd57cbb651716619e084dab9' | apt-key add -
                """,
            ),
            (
                "root",
                # we should have --no-install-recommends on all our apt-get install commands,
                # but here it's important because it will pull in CRAN packages
                # via r-recommends, which is only guaranteed to be compatible with the latest r-base-core
                r"""
                apt-get update > /dev/null && \
                apt-get install --yes --no-install-recommends \
                        r-base-core={R_version} \
                        r-base-dev={R_version} \
                        libclang-dev \
                        libzmq3-dev > /dev/null && \
                apt-get -qq purge && \
                apt-get -qq clean && \
                rm -rf /var/lib/apt/lists/*
                """.format(
                    R_version=self.r_version
                ),
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
                r"""
                sed -i -e '/^R_LIBS_USER=/s/^/#/' /etc/R/Renviron && \
                echo "R_LIBS_USER=${R_LIBS_USER}" >> /etc/R/Renviron
                """,
            ),
            (
                "root",
                # RStudio's CRAN mirror needs this to figure out which binary package to serve.
                # If not set properly, it will just serve up source packages
                # Quite hilarious, IMO.
                # See https://docs.rstudio.com/rspm/1.0.12/admin/binaries.html
                # Set mirror for RStudio too, by modifying rsession.conf
                r"""
                R RHOME && \
                mkdir -p /usr/lib/R/etc /etc/rstudio && \
                echo 'options(repos = c(CRAN = "{cran_mirror_url}"))' > /usr/lib/R/etc/Rprofile.site && \
                echo 'options(HTTPUserAgent = sprintf("R/%s R (%s)", getRversion(), paste(getRversion(), R.version$platform, R.version$arch, R.version$os)))' >> /usr/lib/R/etc/Rprofile.site && \
                echo 'r-cran-repos={cran_mirror_url}' > /etc/rstudio/rsession.conf
                """.format(
                    cran_mirror_url=cran_mirror_url
                ),
            ),
            (
                "${NB_USER}",
                # Install a pinned version of devtools, IRKernel and shiny
                r"""
                R --quiet -e "install.packages(c('devtools', 'IRkernel', 'shiny'), repos='{devtools_cran_mirror_url}')" && \
                R --quiet -e "IRkernel::installspec(prefix='$NB_PYTHON_PREFIX')"
                """.format(
                    devtools_cran_mirror_url=self.get_devtools_snapshot_url()
                ),
            ),
        ]

        return super().get_build_scripts() + scripts

    def get_preassemble_script_files(self):
        files = super().get_preassemble_script_files()
        installR_path = self.binder_path("install.R")
        if os.path.exists(installR_path):
            files[installR_path] = installR_path

        return files

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
                    "Rscript %s && touch /tmp/.preassembled || true && rm -rf /tmp/downloaded_packages"
                    % installR_path,
                )
            ]

        return super().get_preassemble_scripts() + scripts

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
                    """if [ ! -f /tmp/.preassembled ]; then Rscript {}; rm -rf /tmp/downloaded_packages; fi""".format(
                        installR_path
                    ),
                )
            ]

        description_R = "DESCRIPTION"
        if not self.binder_dir and os.path.exists(description_R):
            assemble_scripts += [
                ("${NB_USER}", 'R --quiet -e "devtools::install_local(getwd())"')
            ]

        return assemble_scripts
