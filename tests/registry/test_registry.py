import os
import secrets
import shutil
import socket
import subprocess
import time
from pathlib import Path

import pytest
import requests

from repo2docker.__main__ import make_r2d
from repo2docker.utils import get_free_port

HERE = Path(__file__).parent


@pytest.fixture(scope="session")
def dind(registry, host_ip):
    port = get_free_port()

    # Generate CA certs here so we can securely connect to the docker daemon
    cert_dir = HERE / f"tmp-certs-{secrets.token_hex(8)}"
    cert_dir.mkdir()

    dind_image = "docker:dind"
    subprocess.check_call(["docker", "pull", dind_image])

    cmd = [
        "docker",
        "run",
        "-e",
        "DOCKER_TLS_CERTDIR=/opt/certs",
        "--privileged",
        "--mount",
        f"type=bind,src={cert_dir},dst=/opt/certs",
        "-p",
        f"{port}:2376",
        dind_image,
        "--host",
        "0.0.0.0:2376",
        "--insecure-registry",
        registry,
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(5)

    try:
        yield f"tcp://127.0.0.1:{port}", cert_dir
    finally:
        shutil.rmtree(cert_dir)
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
        s.connect(("10.254.254.254", 1))
        host_ip = s.getsockname()[0]
    finally:
        s.close()

    return host_ip


@pytest.fixture(scope="session")
def registry(host_ip):
    port = get_free_port()
    # Explicitly pull the image first so it runs on time
    registry_image = "registry:3.0.0-rc.3"
    subprocess.check_call(["docker", "pull", registry_image])

    cmd = ["docker", "run", "--rm", "-p", f"{port}:5000", registry_image]
    proc = subprocess.Popen(cmd)
    health_url = f"http://{host_ip}:{port}/v2"
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
    r2d = make_r2d(["--image", image_name, "--push", "--no-run", str(HERE)])

    docker_host, cert_dir = dind
    os.environ["DOCKER_HOST"] = docker_host
    os.environ["DOCKER_CERT_PATH"] = str(cert_dir / "client")
    os.environ["DOCKER_TLS_VERIFY"] = "1"
    r2d.start()

    proc = subprocess.run(["docker", "manifest", "inspect", "--insecure", image_name])
    assert proc.returncode == 0
