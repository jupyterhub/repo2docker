FROM python:3.5

RUN pip install --no-cache notebook

CMD "/bin/sh"

ADD change.sh /usr/local/bin/change.sh

ARG NB_UID
ENV HOME /tmp
WORKDIR ${HOME}

USER $NB_UID
