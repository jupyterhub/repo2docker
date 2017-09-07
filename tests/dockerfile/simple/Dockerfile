FROM python:3.5

ARG JUPYTERHUB_VERSION
RUN pip3 install jupyterhub==$JUPYTERHUB_VERSION

ENTRYPOINT "/bin/sh"

ADD sayhi.sh /usr/local/bin/sayhi.sh
ADD verify verify
