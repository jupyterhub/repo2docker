FROM ubuntu:artful

RUN apt-get update && apt-get install --yes python3

COPY . .
RUN ./postBuild
