ARG PYTHON_VERSION=3.7
FROM python:${PYTHON_VERSION}

# build wheels in first image
ADD . /tmp/src
RUN mkdir /tmp/wheelhouse \
 && cd /tmp/wheelhouse \
 && pip3 wheel --no-cache-dir /tmp/src

# run with slim variant instead of full
# since we won't need compilers and friends
FROM python:${PYTHON_VERSION}-slim

# we do need git, though
# git-lfs is in backports
ARG DEB_RELEASE=stretch
RUN echo "deb http://deb.debian.org/debian ${DEB_RELEASE}-backports main" > /etc/apt/sources.list.d/backports.list \
 && apt-get update \
 && apt-get -t ${DEB_RELEASE}-backports -y install --no-install-recommends git git-lfs \
 && rm -rf /var/lib/apt/lists/*

# install repo2docker
COPY --from=0 /tmp/wheelhouse /tmp/wheelhouse
RUN pip3 install --no-cache-dir /tmp/wheelhouse/*.whl

# add git-credential helper
COPY ./docker/git-credential-env /usr/local/bin/git-credential-env
RUN git config --system credential.helper env

# Used for testing purpose in ports.py
EXPOSE 52000
