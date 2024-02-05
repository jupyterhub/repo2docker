"""
Test if the explict hostname is supplied correctly to the container
"""

import time

import requests

from repo2docker.app import Repo2Docker

# Minimal Dockerfile to make build as fast as possible
DOCKER_FILE = """
FROM python:3.7-slim
# install the notebook package
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache notebook

# create user with a home directory
ARG NB_USER
ARG NB_UID
ENV USER ${NB_USER}
ENV HOME /home/${NB_USER}

RUN adduser --disabled-password \
    --gecos "Default user" \
    --uid ${NB_UID} \
    ${NB_USER}
WORKDIR ${HOME}
USER ${NB_USER}
"""


def test_connect_url(tmpdir):
    tmpdir.chdir()
    p = tmpdir.join("Dockerfile")
    p.write(DOCKER_FILE)

    # we set run=False so that we can start the container ourselves and
    # get a handle to the container, used to inspect the logs
    app = Repo2Docker(repo=str(tmpdir), run=False)
    app.initialize()
    app.start()
    container = app.start_container()

    container_url = f"http://{app.hostname}:{app.port}/api"
    expected_url = f"http://{app.hostname}:{app.port}"

    # wait a bit for the container to be ready
    # give the container a chance to start
    time.sleep(1)

    try:
        # try a few times to connect
        success = False
        for i in range(1, 4):
            container.reload()
            assert container.status == "running"
            if expected_url not in container.logs().decode("utf8"):
                time.sleep(i * 3)
                continue
            try:
                info = requests.get(container_url).json()
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(i * 3)
            else:
                print(info)
                success = True
                break
        assert success, f"Notebook never started in {container}"
    finally:
        # stop the container
        container.stop()
        app.wait_for_container(container)
