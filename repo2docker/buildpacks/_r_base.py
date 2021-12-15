"""
Base information for using R in BuildPacks.

Keeping this in r.py would lead to cyclic imports.
"""

RSTUDIO_URL = "https://download2.rstudio.org/server/bionic/amd64/rstudio-server-2021.09.1-372-amd64.deb"
RSTUDIO_SHA256SUM = "c58df09468870b89f1796445853dce2dacaa0fc5b7bb1f92b036fa8da1d1f8a3"

# Via https://www.rstudio.com/products/shiny/download-server/
SHINY_URL = "https://download3.rstudio.org/ubuntu-14.04/x86_64/shiny-server-1.5.12.933-amd64.deb"
SHINY_CHECKSUM = "9aeef6613e7f58f21c97a4600921340e"

# Version of MRAN to pull devtools from.
DEVTOOLS_VERSION = "2018-02-01"

# IRKernel version - specified as a tag in the IRKernel repository
IRKERNEL_VERSION = "1.1"


def rstudio_base_scripts():
    """Base steps to install RStudio and shiny-server."""
    return [
        (
            "root",
            # Install RStudio!
            r"""
                curl --silent --location --fail {rstudio_url} > /tmp/rstudio.deb && \
                echo '{rstudio_sha256sum} /tmp/rstudio.deb' | sha256sum -c - && \
                apt-get update && \
                apt install -y /tmp/rstudio.deb && \
                rm /tmp/rstudio.deb && \
                apt-get -qq purge && \
                apt-get -qq clean && \
                rm -rf /var/lib/apt/lists/*
                """.format(
                rstudio_url=RSTUDIO_URL, rstudio_sha256sum=RSTUDIO_SHA256SUM
            ),
        ),
        (
            "root",
            # Install Shiny Server!
            r"""
                curl --silent --location --fail {url} > {deb} && \
                echo '{checksum} {deb}' | md5sum -c - && \
                dpkg -i {deb} && \
                rm {deb}
                """.format(
                url=SHINY_URL, checksum=SHINY_CHECKSUM, deb="/tmp/shiny.deb"
            ),
        ),
        (
            "${NB_USER}",
            # Install nbrsessionproxy
            r"""
                pip install --no-cache-dir \
                    'jupyter-rsession-proxy>=2.0' \
                    https://github.com/ryanlovett/jupyter-shiny-proxy/archive/47557dc47e2aeeab490eb5f3eeae414cdde4a6a9.zip
                """,
        ),
        (
            # Not all of these locations are configurable; so we make sure
            # they exist and have the correct permissions
            "root",
            r"""
                install -o ${NB_USER} -g ${NB_USER} -d /var/log/shiny-server && \
                install -o ${NB_USER} -g ${NB_USER} -d /var/lib/shiny-server && \
                install -o ${NB_USER} -g ${NB_USER} /dev/null /var/log/shiny-server.log && \
                install -o ${NB_USER} -g ${NB_USER} /dev/null /var/run/shiny-server.pid
                """,
        ),
    ]
