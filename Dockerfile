ARG ALPINE_VERSION=3.12.0
FROM alpine:${ALPINE_VERSION}

RUN apk add --no-cache git python3 python3-dev py-pip

# build wheels in first image
ADD . /tmp/src
# restore the hooks directory so that the repository isn't marked as dirty
RUN cd /tmp/src && git clean -xfd && git checkout -- hooks && git status
RUN mkdir /tmp/wheelhouse \
 && cd /tmp/wheelhouse \
 && pip3 install wheel \
 && pip3 wheel --no-cache-dir /tmp/src \
 && ls -l /tmp/wheelhouse

FROM alpine:${ALPINE_VERSION}

# install python, git, bash, mercurial
RUN apk add --no-cache git git-lfs python3 py-pip bash docker mercurial

# install hg-evolve (Mercurial extensions)
RUN pip3 install hg-evolve --user --no-cache-dir

# install repo2docker
COPY --from=0 /tmp/wheelhouse /tmp/wheelhouse
RUN pip3 install --no-cache-dir /tmp/wheelhouse/*.whl \
 && pip3 list

# add git-credential helper
COPY ./docker/git-credential-env /usr/local/bin/git-credential-env
RUN git config --system credential.helper env

# Used for testing purpose in ports.py
EXPOSE 52000
