FROM ubuntu:17.04

MAINTAINER Yuvi Panda <yuvipanda@gmail.com>

LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            wget \
            tar \
            ca-certificates \
            bzip2 \
            git \
            locales && \
    apt-get purge && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

ENV CONDA_DIR=/opt/conda \
    PATH=/opt/conda/bin:$PATH \
    NB_USER=jovyan \
    HOME=/home/jovyan

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

WORKDIR $HOME
ADD install-miniconda.bash /tmp/
ADD environment.yml /tmp/

RUN bash /tmp/install-miniconda.bash && \
    rm /tmp/install-miniconda.bash /tmp/environment.yml

USER $NB_USER
COPY ./s2i/bin/ /usr/libexec/s2i

EXPOSE 8888
