"""
Test if the explict hostname is supplied correctly to the container
"""
import os
import sys
import pytest
import requests
import time
import urllib.parse
from repo2docker.app import Repo2Docker

def test_connect_url(tmpdir):
    tmpdir.chdir()
    #q = tmpdir.join("environment.yml")
    #q.write("dependencies:\n"
    #        "  -  notebook==5.6.0")
    p = tmpdir.join("requirements.txt")
    p.write("notebook==5.6.0")

    app = Repo2Docker()
    argv = [str(tmpdir), ]
    app.initialize(argv)
    app.debug = True
    app.run = False
    app.start()  # This just build the image and does not run it.
    container = app.start_container()
    container_url = 'http://{}:{}/api'.format(app.hostname, app.port)
    expected_url = 'http://{}:{}'.format(app.hostname, app.port)

    # wait a bit for the container to be ready
    # give the container a chance to start
    time.sleep(1)

    try:
        # try a few times to connect
        success = False
        for i in range(1, 4):
            container.reload()
            assert container.status == 'running'
            if expected_url not in container.logs().decode("utf8"):
                time.sleep(i * 3)
                continue
            try:
                info = requests.get(container_url).json()
            except Exception as e:
                print("Error: %s" % e)
                time.sleep(i * 3)
            else:
                print(info)
                success = True
                break
        assert success, "Notebook never started in %s" % container
    finally:
        # stop the container
        container.stop()
        app.wait_for_container(container)
