import os
import re
import time
import urllib
import pytest
#import docker

from repo2docker.app import Repo2Docker
from repo2docker.__main__ import make_r2d

VALID = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'versioned', 'valid')
INVALID = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'versioned', 'invalid')

URL = 'https://www.github.com/craig-willis/repo2docker-version-support'

def test_versioned_local_valid():
    """
    Test whether the image built by repo2docker uses the version specified
    in repo2docker.version
    """

    verify_versioned_image(VALID, 'test-verioned-valid')

def test_versioned_local_invalid():
    """
    Test whether the image built by repo2docker uses the version specified
    in repo2docker.version
    """

    with pytest.raises(urllib.error.HTTPError):
       verify_versioned_image(INVALID, 'test-versioned-invalid')

def test_versioned_github():
    """
    Test whether the image built by repo2docker uses the version specified
    in repo2docker.version
    """
    verify_versioned_image(URL, 'test-versioned-remote')

def verify_versioned_image(path, image_name):
    """
    Test whether the image built by repo2docker uses the version specified
    in repo2docker.version
    """

    # Not sure why I need to provide the user-id and name?
    #app = make_r2d(['--no-run', '--image-name', image_name, '--user-id=1000', '--user-name=jovyan', path])
    app = make_r2d(['--no-run', '--user-id=1000', '--user-name=jovyan', path])
    app.initialize()
    app.build()

    # First thought was to use the image labels, but these were added too
    # recently!
    #client = docker.from_env(version="auto")
    #print(client.images.get("test-versioned").labels)

    # For repo2docker v0.5,  confirm that the release used to build the image is ubuntu artful
    container = app.start_container()
    time.sleep(1)
    try:
        status, output = container.exec_run(['sh', '-c', 'grep DISTRIB_CODENAME /etc/lsb-release | cut -f2 -d='])
        assert status != 1
        assert re.match('artful', output.decode("utf-8"))
    finally:
        # stop the container
        container.stop()
        app.wait_for_container(container)

