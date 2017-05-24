FROM ubuntu:17.04

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            curl \
            python3 \
            python3-pip \
            python3-setuptools \
            git && \
    apt-get clean && apt-get purge

COPY install-s2i.bash /usr/local/bin/install-s2i.bash
RUN /usr/local/bin/install-s2i.bash

RUN pip3 install --upgrade pip wheel

RUN mkdir /tmp/src
ADD . /tmp/src
RUN pip3 install /tmp/src

