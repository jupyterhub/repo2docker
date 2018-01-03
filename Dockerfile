FROM python:3.6.3

RUN mkdir /tmp/src
ADD . /tmp/src
RUN pip3 install --no-cache-dir /tmp/src
RUN cp /tmp/src/docker/git-credential-env /usr/local/bin/git-credential-env && \
    git config --system credential.helper env
