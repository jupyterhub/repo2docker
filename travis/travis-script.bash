#!/bin/bash
set -eu -o pipefail

VERSION=$(git rev-parse --short HEAD)

IMAGE="jupyter/repo2docker:${VERSION}"
docker build -t ${IMAGE} .

if [[ "$TRAVIS_PULL_REQUEST" == "false" ]]; then
    docker login -u ${DOCKER_LOGIN} -p "${DOCKER_PASSWORD}"
    docker push ${IMAGE}
    echo "Pushed new repo2docker image: ${IMAGE}"
fi
