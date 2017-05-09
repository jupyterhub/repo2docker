FROM ubuntu:16.10

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

RUN pip3 install --no-cache-dir git+https://github.com/yuvipanda/builder@e7d51c3

