FROM python:3.6.3-alpine3.6


RUN mkdir /tmp/src
ADD . /tmp/src
RUN pip3 install --no-cache-dir /tmp/src

