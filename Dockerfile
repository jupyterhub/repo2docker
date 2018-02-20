FROM python:3.6.3

# Used for testing purpose in ports.py
EXPOSE 52000
RUN mkdir /tmp/src
ADD . /tmp/src
RUN pip3 install --no-cache-dir /tmp/src
RUN cp /tmp/src/docker/git-credential-env /usr/local/bin/git-credential-env && \
    git config --system credential.helper env
