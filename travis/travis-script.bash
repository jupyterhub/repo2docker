#!/bin/bash
set -eu -o pipefail

VERSION=$(git rev-parse --short HEAD)

IMAGE="jupyter/repo2docker:${VERSION}"
docker build -t ${IMAGE} .

if [[ "$TRAVIS_PULL_REQUEST" == "false" ]]; then
    docker login -u ${DOCKER_LOGIN} -p "${DOCKER_PASSWORD}"
    docker push ${IMAGE}
    echo "Pushed new repo2docker image: ${IMAGE}"
    if [[ ! -z "${TRAVIS_TAG}" ]]; then
        # also push tagged versions
        IMAGE_TAG="jupyter/repo2docker:${TRAVIS_TAG/v/}"
        docker tag "${IMAGE}" "${IMAGE_TAG}"
        docker push "${IMAGE_TAG}"
        echo "Pushed new repo2docker image: ${IMAGE_TAG}"
    fi
fi
