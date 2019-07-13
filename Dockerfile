ARG ALPINE_VERSION=3.9.4
FROM alpine:${ALPINE_VERSION}

RUN apk add --no-cache git python3 python3-dev

# build wheels in first image
ADD . /tmp/src
RUN mkdir /tmp/wheelhouse \
 && cd /tmp/wheelhouse \
 && pip3 install wheel \
 && pip3 wheel --no-cache-dir /tmp/src

FROM alpine:${ALPINE_VERSION}

# install python, git, bash
RUN apk add --no-cache git git-lfs python3 bash

# install repo2docker
COPY --from=0 /tmp/wheelhouse /tmp/wheelhouse
RUN pip3 install --no-cache-dir /tmp/wheelhouse/*.whl

# add git-credential helper
COPY ./docker/git-credential-env /usr/local/bin/git-credential-env
RUN git config --system credential.helper env

# Used for testing purpose in ports.py
EXPOSE 52000
