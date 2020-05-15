"""
Base information for using R in BuildPacks.

Keeping this in r.py would lead to cyclic imports.
"""

# Via https://rstudio.com/products/rstudio/download-server/debian-ubuntu/
RSTUDIO_URL = "https://download2.rstudio.org/server/bionic/amd64/rstudio-server-1.2.5001-amd64.deb"
# This is MD5, because that is what RStudio download page provides!
RSTUDIO_CHECKSUM = "d33881b9ab786c09556c410e7dc477de"

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
                echo '{rstudio_checksum} /tmp/rstudio.deb' | md5sum -c - && \
                apt-get update && \
                apt install -y /tmp/rstudio.deb && \
                rm /tmp/rstudio.deb && \
                apt-get -qq purge && \
                apt-get -qq clean && \
                rm -rf /var/lib/apt/lists/*
                """.format(
                rstudio_url=RSTUDIO_URL, rstudio_checksum=RSTUDIO_CHECKSUM
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
                pip install --no-cache-dir jupyter-server-proxy==1.4.0 && \
                pip install --no-cache-dir https://github.com/jupyterhub/jupyter-rsession-proxy/archive/d5efed5455870556fc414f30871d0feca675a4b4.zip && \
                pip install --no-cache-dir https://github.com/ryanlovett/jupyter-shiny-proxy/archive/47557dc47e2aeeab490eb5f3eeae414cdde4a6a9.zip && \
                jupyter serverextension enable jupyter_server_proxy --sys-prefix && \
                jupyter nbextension install --py jupyter_server_proxy --sys-prefix && \
                jupyter nbextension enable --py jupyter_server_proxy --sys-prefix
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
