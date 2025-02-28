import os
import socket
from pathlib import Path
import subprocess
import pytest
from repo2docker.__main__ import make_r2d
from repo2docker.utils import get_free_port
import time
import requests
import secrets

HERE = Path(__file__).parent

@pytest.fixture(scope="session")
def dind(registry, host_ip):
    port = get_free_port()
    dind_image = "docker:dind"
    subprocess.check_call(["docker", "pull", dind_image])
    # This is insecure, because I'm disabling all kinds of authentication on the docker daemon.
    # FIXME: Use TLS verification.
    # but also docker this is your own fucking fault for making technical choices that force dockerhub
    # to be the primary registry, so your registry handling sucks and forces these kinds of difficulties.
    cmd = [
        "docker", "run", "-e", 'DOCKER_TLS_CERTDIR=',
        "--privileged", "-p", f"{port}:2376", dind_image,
        "--host", "0.0.0.0:2376",
        "--insecure-registry", registry,
        "--tls=false"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(5)

    try:
        yield f"tcp://{host_ip}:{port}"
    finally:
        proc.terminate()
        proc.wait()

@pytest.fixture(scope="session")
def host_ip():
    # Get the IP of the current machine, as we need to use the same IP
    # for all our docker commands, *and* the dind we run needs to reach it
    # in the same way.
    # Thanks to https://stackoverflow.com/a/28950776
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        host_ip = s.getsockname()[0]
    finally:
        s.close()

    return host_ip

@pytest.fixture(scope="session")
def registry(host_ip):
    port = get_free_port()
    # Explicitly pull the image first so it runs on time
    registry_image =  "registry:3.0.0-rc.3"
    subprocess.check_call(["docker", "pull", registry_image])


    cmd = [
        "docker", "run", "--rm",
        "-p", f"{port}:5000", registry_image
    ]
    proc = subprocess.Popen(cmd)
    health_url = f'http://{host_ip}:{port}/v2'
    # Wait for the registry to actually come up
    for i in range(10):
        try:
            resp = requests.get(health_url)
            if resp.status_code in (401, 200):
                break
        except requests.ConnectionError:
            # The service is not up yet
            pass
        time.sleep(i)
    else:
        raise TimeoutError("Test registry did not come up in time")

    try:
        yield f"{host_ip}:{port}"
    finally:
        proc.terminate()
        proc.wait()


def test_registry(registry, dind):
    image_name = f"{registry}/{secrets.token_hex(8)}:latest"
    r2d = make_r2d([
        "--image", image_name,
        "--push", "--no-run", str(HERE)
    ])

    os.environ["DOCKER_HOST"] = dind
    r2d.start()

    proc = subprocess.run(["docker", "manifest", "inspect", "--insecure", image_name])
    assert proc.returncode == 0
