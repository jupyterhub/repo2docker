FROM python:3.10

RUN pip install --no-cache notebook

CMD "/bin/sh"

ADD sayhi.sh /usr/local/bin/sayhi.sh
ADD verify verify

ARG NB_UID
ENV HOME /tmp
USER $NB_UID
