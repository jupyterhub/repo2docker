# syntax = docker/dockerfile:1.3
ARG ALPINE_VERSION=3.16
FROM alpine:${ALPINE_VERSION} AS builder

RUN apk add --no-cache git python3 python3-dev py-pip build-base

# set pip's cache directory using this environment variable, and use
# ARG instead of ENV to ensure its only set when the image is built
ARG PIP_CACHE_DIR=/tmp/pip-cache

# build wheels in first image
ADD . /tmp/src
RUN cd /tmp/src && git clean -xfd && git status
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    mkdir /tmp/wheelhouse \
 && cd /tmp/wheelhouse \
 && pip3 install wheel \
 && pip3 wheel /tmp/src \
 && ls -l /tmp/wheelhouse

FROM alpine:${ALPINE_VERSION}

# install python, git, bash, mercurial
RUN apk add --no-cache git git-lfs python3 py-pip bash docker mercurial

# repeat ARG from above
ARG PIP_CACHE_DIR=/tmp/pip-cache

# install repo2docker
# and hg-evolve (Mercurial extensions)
# mount /tmp/wheelhouse from build stage
# avoids extra layer when using COPY --from
RUN --mount=type=cache,target=${PIP_CACHE_DIR} \
    --mount=type=cache,from=builder,source=/tmp/wheelhouse,target=/tmp/wheelhouse \
    pip3 install --ignore-installed --no-deps /tmp/wheelhouse/*.whl \
 && pip3 install hg-evolve \
 && pip3 list

# add git-credential helper
COPY ./docker/git-credential-env /usr/local/bin/git-credential-env
RUN git config --system credential.helper env

# add entrypoint
COPY ./docker/entrypoint /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint"]

# Used for testing purpose in ports.py
EXPOSE 52000
