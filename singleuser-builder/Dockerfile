FROM ubuntu:16.10

MAINTAINER Yuvi Panda <yuvipanda@gmail.com>

LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

ENV APP_DIR /srv/app

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            python3 \
            python3-venv \
            tar \
            git && \
    apt-get purge && apt-get clean

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN mkdir -p ${APP_DIR} && chown -R jovyan:jovyan /srv/app

WORKDIR ${APP_DIR}

USER jovyan
RUN python3 -m venv venv

# FIXME: Specify actual versions here
RUN ${APP_DIR}/venv/bin/pip install --no-cache-dir jupyter jupyterhub

COPY ./s2i/bin/ /usr/libexec/s2i

EXPOSE 8888
