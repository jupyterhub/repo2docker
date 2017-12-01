FROM ubuntu:zesty

RUN apt-get update && apt-get install --yes python3

COPY . .
RUN ./postBuild
