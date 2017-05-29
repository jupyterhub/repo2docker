FROM ubuntu:17.04

MAINTAINER Yuvi Panda <yuvipanda@gmail.com>

LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

ENV APP_DIR /srv/app
ENV PATH ${APP_DIR}/venv/bin:$PATH

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            python3 \
            python3-venv \
            tar \
            git \
            locales && \
    apt-get purge && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN mkdir -p ${APP_DIR} && chown -R jovyan:jovyan ${APP_DIR}

WORKDIR /home/jovyan

USER jovyan
RUN python3 -m venv ${APP_DIR}/venv

RUN ${APP_DIR}/venv/bin/pip install --no-cache-dir notebook==5.0.0 jupyterhub==0.7.2 ipywidgets==5.2.3 && \
    ${APP_DIR}/venv/bin/jupyter nbextension enable --py widgetsnbextension

COPY ./s2i/bin/ /usr/libexec/s2i

EXPOSE 8888
