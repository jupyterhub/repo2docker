FROM buildpack-deps:bionic

# avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Set up locales properly
RUN apt-get -qq update && \
    apt-get -qq install --yes --no-install-recommends locales > /dev/null && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Use bash as default shell, rather than sh
ENV SHELL /bin/bash

# Set up user
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}

RUN wget --quiet -O - https://deb.nodesource.com/gpgkey/nodesource.gpg.key |  apt-key add - && \
    DISTRO="bionic" && \
    echo "deb https://deb.nodesource.com/node_10.x $DISTRO main" >> /etc/apt/sources.list.d/nodesource.list && \
    echo "deb-src https://deb.nodesource.com/node_10.x $DISTRO main" >> /etc/apt/sources.list.d/nodesource.list

# Base package installs are not super interesting to users, so hide their outputs
# If install fails for some reason, errors will still be printed
RUN apt-get -qq update && \
    apt-get -qq install --yes --no-install-recommends \
       {% for package in base_packages -%}
       {{ package }} \
       {% endfor -%}
    > /dev/null && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*

{% if packages -%}
RUN apt-get -qq update && \
    apt-get -qq install --yes \
       {% for package in packages -%}
       {{ package }} \
       {% endfor -%}
    > /dev/null && \
    apt-get -qq purge && \
    apt-get -qq clean && \
    rm -rf /var/lib/apt/lists/*
{% endif -%}

EXPOSE 8888

{% if build_env -%}
# Environment variables required for build
{% for item in build_env -%}
ENV {{item[0]}} {{item[1]}}
{% endfor -%}
{% endif -%}

{% if path -%}
# Special case PATH
ENV PATH {{ ':'.join(path) }}:${PATH}
{% endif -%}

{% if build_script_files -%}
# If scripts required during build are present, copy them
{% for src, dst in build_script_files.items() %}
COPY {{ src }} {{ dst }}
{% endfor -%}
{% endif -%}

{% for sd in build_script_directives -%}
{{sd}}
{% endfor %}

# Allow target path repo is cloned to be configurable
ARG REPO_DIR=${HOME}
ENV REPO_DIR ${REPO_DIR}
WORKDIR ${REPO_DIR}

# We want to allow two things:
#   1. If there's a .local/bin directory in the repo, things there
#      should automatically be in path
#   2. postBuild and users should be able to install things into ~/.local/bin
#      and have them be automatically in path
#
# The XDG standard suggests ~/.local/bin as the path for local user-specific
# installs. See https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html
ENV PATH ${HOME}/.local/bin:${REPO_DIR}/.local/bin:${PATH}

# Copy and chown stuff. This doubles the size of the repo, because
# you can't actually copy as USER, only as root! Thanks, Docker!
USER root
COPY src/ ${REPO_DIR}
RUN chown -R ${NB_USER}:${NB_USER} ${REPO_DIR}

{% if env -%}
# The rest of the environment
{% for item in env -%}
ENV {{item[0]}} {{item[1]}}
{% endfor -%}
{% endif -%}


# Run assemble scripts! These will actually build the specification
# in the repository into the image.
{% for sd in assemble_script_directives -%}
{{ sd }}
{% endfor %}

# Container image Labels!
# Put these at the end, since we don't want to rebuild everything
# when these change! Did I mention I hate Dockerfile cache semantics?
{% for k, v in labels.items() %}
LABEL {{k}}="{{v}}"
{%- endfor %}

# We always want containers to run as non-root
USER ${NB_USER}

{% if post_build_scripts -%}
# Make sure that postBuild scripts are marked executable before executing them
{% for s in post_build_scripts -%}
RUN chmod +x {{ s }}
RUN ./{{ s }}
{% endfor %}
{% endif -%}

# Add start script
{% if start_script is not none -%}
RUN chmod +x "{{ start_script }}"
ENTRYPOINT ["{{ start_script }}"]
{% endif -%}

# Add healtcheck script
#HEALTHCHECK --interval=5s --timeout=15s --start-period=5s CMD python3 /healthcheck.py 8888


# Specify the default command to run
CMD ["jupyter", "notebook", "--ip", "0.0.0.0"]

{% if appendix -%}
# Appendix:
{{ appendix }}
{% endif %}
