"""
Test if the environment.yml is empty or it constains other data structure than a dictionary
"""
import os
import sys
import pytest
import requests
import time
from repo2docker.app import Repo2Docker

def test_env_yml(tmpdir):
    tmpdir.chdir()
    #q = tmpdir.join("environment.yml")
    #q.write("dependencies:\n"
    #        "  -  notebook==5.6.0rc1")
    p = tmpdir.join("requirements.txt")
    p.write("notebook==5.6.0rc1")

    app = Repo2Docker()
    argv = [str(tmpdir), ]
    app.initialize(argv)
    app.run = False
    app.start()  # This just build the image and does not run it.
    detect = app.build
    print("app.build",detect)
    container = app.start_container()
    port = app.port
    print("port in test", port)
    hostname = app.hostname
    # wait a bit for the container to be ready
    container_url = 'http://{}:{}/api'.format(hostname, port)
    print("print container url",container_url)
    # wait a bit for the container to be ready
    # give the container a chance to start
    time.sleep(1)
    try:
        # try a few times to connect
        success = False
        for i in range(1, 4):
            container.reload()
            assert container.status == 'running'
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
