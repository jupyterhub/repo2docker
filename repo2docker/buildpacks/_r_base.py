"""
Base information for using R in BuildPacks.

Keeping this in r.py would lead to cyclic imports.
"""

from ..semver import parse_version as V


def rstudio_base_scripts(r_version):
    """Base steps to install RStudio and shiny-server."""

    # Shiny server (not the package!) seems to be the same version for all R versions
    shiny_server_url = "https://download3.rstudio.org/ubuntu-18.04/x86_64/shiny-server-1.5.22.1017-amd64.deb"
    shiny_proxy_version = "1.3"
    shiny_sha256sum = "0fa40054f038de464a26f3f8c40180a072228454762b7a12ed50568b3256c236"

    # RStudio server has different builds based on wether OpenSSL 3 or 1.1 is available in the base
    # image. 3 is present Jammy+, 1.1 until then. Instead of hardcoding URLs based on distro, we actually
    # check for the dependency itself directly in the code below. You can find these URLs in
    # https://posit.co/download/rstudio-server/, toggling between Ubuntu 22 (for openssl3) vs earlier versions (openssl 1.1)
    # you may forget about openssl, but openssl never forgets you.
    rstudio_openssl3_url = "https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2022.12.0-353-amd64.deb"
    rstudio_openssl3_sha256sum = (
        "a5aa2202786f9017a6de368a410488ea2e4fc6c739f78998977af214df0d6288"
    )

    rstudio_openssl1_url = "https://download2.rstudio.org/server/bionic/amd64/rstudio-server-2022.12.0-353-amd64.deb"
    rstudio_openssl1_sha256sum = (
        "bb88e37328c304881e60d6205d7dac145525a5c2aaaf9da26f1cb625b7d47e6e"
    )
    rsession_proxy_version = "2.2.0"

    return [
        (
            "root",
            # we should have --no-install-recommends on all our apt-get install commands,
            # but here it's important because these recommend r-base,
            # which will upgrade the installed version of R, undoing our pinned version
            rf"""
            apt-get update > /dev/null && \
            if apt-cache search libssl3 | grep -q libssl3; then \
              RSTUDIO_URL="{rstudio_openssl3_url}" ;\
              RSTUDIO_HASH="{rstudio_openssl3_sha256sum}" ;\
            else \
              RSTUDIO_URL="{rstudio_openssl1_url}" ;\
              RSTUDIO_HASH="{rstudio_openssl1_sha256sum}" ;\
            fi && \
            curl --silent --location --fail ${{RSTUDIO_URL}} > /tmp/rstudio.deb && \
            curl --silent --location --fail {shiny_server_url} > /tmp/shiny.deb && \
            echo "${{RSTUDIO_HASH}} /tmp/rstudio.deb" | sha256sum -c - && \
            echo '{shiny_sha256sum} /tmp/shiny.deb' | sha256sum -c - && \
            apt install -y --no-install-recommends /tmp/rstudio.deb /tmp/shiny.deb && \
            rm /tmp/*.deb && \
            apt-get -qq purge && \
            apt-get -qq clean && \
            rm -rf /var/lib/apt/lists/*
            """,
        ),
        (
            "${NB_USER}",
            # Install jupyter-rsession-proxy
            rf"""
                pip install --no-cache \
                    jupyter-rsession-proxy=={rsession_proxy_version} \
                    jupyter-shiny-proxy=={shiny_proxy_version}
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
