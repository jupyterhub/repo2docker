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

    It currently sets up R from the ubuntu repository being used. This
    is unideal, and we should investigate other solutions!
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

        Note that we explicitly do *not* check if a requirements.txt
        is present here (by calling super().detect()).
        """
        return bool(self.checkpoint_date)

    def get_path(self):
        return super().get_path() + [
            '/usr/lib/rstudio-server/bin/'
        ]

    def get_env(self):
        return super().get_env() + [
            # This is the path where user libraries are installed
            ('R_LIBS_USER', '${APP_BASE}/rlibs')
        ]

    def get_packages(self):
        return super().get_packages().union([
            'r-base',
            # For rstudio
            'psmisc',
            'libapparmor1',
            'sudo',
            'lsb-release'
        ])

    def get_build_scripts(self):
        mran_url = 'https://mran.microsoft.com/snapshot/{}'.format(
            self.checkpoint_date.isoformat()
        )
        rstudio_url = 'https://download2.rstudio.org/rstudio-server-1.1.419-amd64.deb'
        # This is MD5, because that is what RStudio download page provides!
        rstudio_checksum = '24cd11f0405d8372b4168fc9956e0386'
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
                # We set the default CRAN repo to the MRAN one at given date
                # We set download method to be curl so we get HTTPS support
                r"""
                echo "options(repos = c(CRAN='{mran_url}'), download.file.method = 'libcurl')" > /etc/R/Rprofile.site
                """.format(mran_url=mran_url)
            ),
            (
                "root",
                # Install RStudio!
                r"""
                curl -L --fail {rstudio_url} > /tmp/rstudio.deb && \
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
                # Install a pinned version of IRKernel and set it up for use!
                r"""
                R --quiet -e "install.packages('devtools')" && \
                R --quiet -e "devtools::install_github('IRkernel/IRkernel', ref='0.8.11')" && \
                R --quiet -e "IRkernel::installspec(prefix='${NB_PYTHON_PREFIX}')"
                """
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
            )

        ]

    def get_assemble_scripts(self):
        assemble_scripts = super().get_assemble_scripts()
        if os.path.exists('install.R'):
            assemble_scripts += [
                (
                    "${NB_USER}",
                    "Rscript install.R"
                )
            ]

        return assemble_scripts
