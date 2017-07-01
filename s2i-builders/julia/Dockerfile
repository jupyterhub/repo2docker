FROM ubuntu:17.04

MAINTAINER Yuvi Panda <yuvipanda@gmail.com>

LABEL io.openshift.s2i.scripts-url=image:///usr/libexec/s2i

ENV APP_DIR /srv/app
ENV JULIA_PATH /usr/local/julia
ENV JULIA_PKGDIR ${APP_DIR}/.julia
ENV JUPYTER ${APP_DIR}/venv/bin/jupyter
ENV PATH ${APP_DIR}/venv/bin:$PATH:${JULIA_PATH}/bin

RUN apt-get update && \
    apt-get install --yes \
            python3 \
            python3-venv \
            python3-dev \
            build-essential \
            pkg-config \
            libfreetype6-dev \
            libpng-dev \
            tar \
            git \
            curl \
            locales && \
    apt-get purge && apt-get clean

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN adduser --disabled-password --gecos "Default Jupyter user" jovyan

RUN mkdir -p ${APP_DIR} && chown -R jovyan:jovyan ${APP_DIR}

# Install Julia
ENV JULIA_PATH /usr/local/julia
ENV JULIA_VERSION 0.6.0

RUN mkdir $JULIA_PATH  && \
    curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1

WORKDIR /home/jovyan

USER jovyan
RUN python3 -m venv ${APP_DIR}/venv

RUN pip install --no-cache-dir notebook==5.0.0 jupyterhub==0.7.2 ipywidgets==5.2.3 jupyterlab==0.22.1 && \
    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
    jupyter serverextension enable --py jupyterlab --sys-prefix

RUN julia -e 'Pkg.init(); Pkg.add("IJulia")' && \
    mv ${HOME}/.local/share/jupyter/kernels/julia-0.6/ ${APP_DIR}/venv/share/jupyter/kernels/julia-0.6


COPY ./s2i/bin/ /usr/libexec/s2i

EXPOSE 8888
