FROM ubuntu:17.04

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
            python3 \
            python3-pip \
            python3-setuptools \
            git && \
    apt-get clean && apt-get purge

RUN mkdir /tmp/src
ADD . /tmp/src
RUN pip3 install --no-cache-dir /tmp/src

