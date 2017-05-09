FROM ubuntu:16.10

MAINTAINER Yuvi Panda <yuvipanda@gmail.com>

LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            wget \
            tar \
            ca-certificates \
            bzip2 \
            git && \
    apt-get purge && apt-get clean

ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/envs/base/bin:$CONDA_DIR/bin/:$PATH
ENV NB_USER jovyan

RUN adduser --disabled-password --gecos "Default Jupyter user" ${NB_USER}

WORKDIR /home/${NB_USER}
ADD install-miniconda.bash /usr/local/bin/install-miniconda.bash

RUN /usr/local/bin/install-miniconda.bash

USER $NB_USER
ADD environment.yml .
RUN conda env create --quiet -n base && conda clean -tipsy
RUN rm environment.yml

COPY ./s2i/bin/ /usr/libexec/s2i

EXPOSE 8888
