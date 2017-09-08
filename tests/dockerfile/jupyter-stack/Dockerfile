FROM jupyter/base-notebook:b4dd11e16ae4

ARG JUPYTERHUB_VERSION
RUN pip install jupyterhub==$JUPYTERHUB_VERSION

RUN pip install there
ADD verify verify
