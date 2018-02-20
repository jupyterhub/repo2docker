import re
import os
import datetime

from .python import PythonBuildPack

class RBuildPack(PythonBuildPack):
    """
    Setup R for use with a repository

    This sets up R + RStudio + IRKernel for a repository that contains:

    1. A `runtime.txt` file with the text:

       r-<year>-<month>-<date>

       Where 'year', 'month' and 'date' refer to a specific
       date snapshot of https://mran.microsoft.com/timemachine
       from which libraries are to be installed.

    2. An optional `install.R` file that will be executed at build time,
       and can be used for installing packages from both MRAN and GitHub.

    The `r-base` package from Ubuntu apt repositories is used to install
    R itself, rather than any of the methods from https://cran.r-project.org/.
    """
    @property
    def runtime(self):
        """
        Return contents of runtime.txt if it exists, '' otherwise
        """
        if not hasattr(self, '_runtime'):
            runtime_path = self.binder_path('runtime.txt')
            try:
                with open(runtime_path) as f:
                    self._runtime = f.read().strip()
            except FileNotFoundError:
                self._runtime = ''

        return self._runtime

    @property
    def checkpoint_date(self):
        """
        Return the date of MRAN checkpoint to use for this repo

        Returns '' if no date is specified
        """
        if not hasattr(self, '_checkpoint_date'):
            match = re.match(r'r-(\d\d\d\d)-(\d\d)-(\d\d)', self.runtime)
            if not match:
                self._checkpoint_date = False
            else:
                self._checkpoint_date = datetime.date(*[int(s) for s in match.groups()])

        return self._checkpoint_date

    def detect(self):
        """
        Check if current repo should be built with the R Build pack

        super().detect() is not called in this function - it would return false
        unless a `requirements.txt` is present and we do not want to require the
        presence of a `requirements.txt` to use R.

        Instead we just check if runtime.txt contains a string of the form
        `r-<YYYY>-<MM>-<DD>`
        """
        # If no date is found, then self.checkpoint_date will be False
        # Otherwise, it'll be a date object, which will evaluate to True
        return bool(self.checkpoint_date)

    def get_path(self):
        """
        Return paths to be added to the PATH environment variable.

        The RStudio package installs its binaries in a non-standard path,
        so we explicitly add that path to PATH.
        """
        return super().get_path() + [
            '/usr/lib/rstudio-server/bin/'
        ]

    def get_env(self):
        """
        Return environment variables to be set.

        We want libraries to be installed in a path that users can write to
        without needing root. This is set via the `R_LIBS_USER` environment
        variable, so we set that here.
        """
        return super().get_env() + [
            # This is the path where user libraries are installed
            ('R_LIBS_USER', '${APP_BASE}/rlibs')
        ]

    def get_packages(self):
        """
        Return list of packages to be installed.

        We install a base version of R, and packages required for RStudio to
        be installed.
        """
        return super().get_packages().union([
            'r-base',
            # For rstudio
            'psmisc',
            'libapparmor1',
            'sudo',
            'lsb-release'
        ])

    def get_build_scripts(self):
        """
        Return series of build-steps common to all R repositories

        All scripts here should be independent of contents of the repository.

        This sets up:

        - A directory owned by non-root in ${R_LIBS_USER} for installing R packages into
        - RStudio
        - R's devtools package, at a particular frozen version (determined by MRAN)
        - IRKernel
        - nbrsessionproxy (to access RStudio via Jupyter Notebook)
        """
        rstudio_url = 'https://download2.rstudio.org/rstudio-server-1.1.419-amd64.deb'
        # This is MD5, because that is what RStudio download page provides!
        rstudio_checksum = '24cd11f0405d8372b4168fc9956e0386'

        # Version of MRAN to pull devtools from.
        devtools_version = '2018-02-01'

        # IRKernel version - specified as a tag in the IRKernel repository
        irkernel_version = '0.8.11'

        return super().get_build_scripts() + [
            (
                "root",
                r"""
                mkdir -p ${R_LIBS_USER} && \
                chown -R ${NB_USER}:${NB_USER} ${R_LIBS_USER}
                """
            ),
            (
                "root",
                # Install RStudio!
                r"""
                curl --silent --location --fail {rstudio_url} > /tmp/rstudio.deb && \
                echo '{rstudio_checksum} /tmp/rstudio.deb' | md5sum -c - && \
                dpkg -i /tmp/rstudio.deb && \
                rm /tmp/rstudio.deb
                """.format(
                    rstudio_url=rstudio_url,
                    rstudio_checksum=rstudio_checksum
                )
            ),
            (
                "${NB_USER}",
                # Install nbrsessionproxy
                r"""
                pip install --no-cache-dir nbrsessionproxy==0.6.1 && \
                jupyter serverextension enable nbrsessionproxy --sys-prefix && \
                jupyter nbextension install --py nbrsessionproxy --sys-prefix && \
                jupyter nbextension enable --py nbrsessionproxy --sys-prefix
                """
            ),
            (
                "${NB_USER}",
                # Install a pinned version of IRKernel and set it up for use!
                r"""
                R --quiet -e "install.packages('devtools', repos='https://mran.microsoft.com/snapshot/{devtools_version}', method='libcurl')" && \
                R --quiet -e "devtools::install_github('IRkernel/IRkernel', ref='{irkernel_version}')" && \
                R --quiet -e "IRkernel::installspec(prefix='$NB_PYTHON_PREFIX')"
                """.format(
                    devtools_version=devtools_version,
                    irkernel_version=irkernel_version
                )
            )
        ]

    def get_assemble_scripts(self):
        """
        Return series of build-steps specific to this repository

        We set the snapshot date used to install R libraries from based on the
        contents of runtime.txt, and run the `install.R` script if it exists.
        """
        mran_url = 'https://mran.microsoft.com/snapshot/{}'.format(
            self.checkpoint_date.isoformat()
        )
        assemble_scripts = super().get_assemble_scripts() + [
            (
                "root",
                # We set the default CRAN repo to the MRAN one at given date
                # We set download method to be curl so we get HTTPS support
                r"""
                echo "options(repos = c(CRAN='{mran_url}'), download.file.method = 'libcurl')" > /etc/R/Rprofile.site
                """.format(mran_url=mran_url)
            ),
        ]

        if os.path.exists('install.R'):
            assemble_scripts += [
                (
                    "${NB_USER}",
                    "Rscript install.R"
                )
            ]

        return assemble_scripts
