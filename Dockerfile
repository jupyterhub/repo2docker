# syntax = docker/dockerfile:1.3
ARG ALPINE_VERSION=3.17
FROM alpine:${ALPINE_VERSION}

RUN apk add --no-cache git python3 python3-dev py3-pip py3-setuptools build-base

# build wheels in first image
ADD . /tmp/src
RUN cd /tmp/src && git clean -xfd && git status
RUN mkdir /tmp/wheelhouse \
 && cd /tmp/wheelhouse \
 && pip3 install wheel \
 && pip3 wheel --no-cache-dir /tmp/src \
 && ls -l /tmp/wheelhouse

FROM alpine:${ALPINE_VERSION}

# install python, git, bash, mercurial, ssh
RUN apk add --no-cache git git-lfs python3 py3-pip py3-setuptools bash docker mercurial openssh

# install hg-evolve (Mercurial extensions)
RUN pip3 install hg-evolve --user --no-cache-dir

# install repo2docker
COPY --from=0 /tmp/wheelhouse /tmp/wheelhouse
RUN pip3 install --no-cache-dir --ignore-installed --no-deps /tmp/wheelhouse/*.whl \
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
