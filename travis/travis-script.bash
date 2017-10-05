#!/bin/bash
set -eu -o pipefail

VERSION=$(git rev-parse --short HEAD)

docker build -t jupyter/repo2docker:${VERSION} .

if [[ "$TRAVIS_PULL_REQUEST" == "false" ]]; then
    docker login -u ${DOCKER_LOGIN} -p "${DOCKER_PASSWORD}"
    docker push jupyter/rep2docker:${VERSION}
fi
