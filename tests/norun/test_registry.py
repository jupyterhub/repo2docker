import json
import os
import secrets
import shutil
import socket
import subprocess
import time
from base64 import b64encode
from pathlib import Path
from tempfile import TemporaryDirectory

import bcrypt
import pytest
import requests

from repo2docker.__main__ import make_r2d
from repo2docker.utils import get_free_port

HERE = Path(__file__).parent


@pytest.fixture(scope="session")
def dind(registry):
    port = get_free_port()
    registry_host, _, _ = registry

    # docker daemon will generate certs here, that we can then use to connect to it.
    # put it in current dir than in /tmp because on macos, current dir is likely to
    # shared with docker VM so it can be mounted, unlike /tmp
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
        registry_host,
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(5)

    try:
        yield f"tcp://127.0.0.1:{port}", cert_dir
    finally:
        try:
            shutil.rmtree(cert_dir)
        except PermissionError:
            # Sometimes this is owned by root in CI. is ok, let's let it go
            pass
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
    username = "user"
    password = secrets.token_hex(16)
    bcrypted_pw = bcrypt.hashpw(
        password.encode("utf-8"), bcrypt.gensalt(rounds=12)
    ).decode("utf-8")

    # We put our password here, and mount it into the container.
    # put it in current dir than in /tmp because on macos, current dir is likely to
    # shared with docker VM so it can be mounted, unlike /tmp
    htpasswd_dir = HERE / f"tmp-certs-{secrets.token_hex(8)}"
    htpasswd_dir.mkdir()
    (htpasswd_dir / "htpasswd.conf").write_text(f"{username}:{bcrypted_pw}")

    # Explicitly pull the image first so it runs on time
    registry_image = "registry:3.0.0-rc.3"
    subprocess.check_call(["docker", "pull", registry_image])

    cmd = [
        "docker",
        "run",
        "--rm",
        "-e",
        "REGISTRY_AUTH=htpasswd",
        "-e",
        "REGISTRY_AUTH_HTPASSWD_REALM=basic",
        "-e",
        "REGISTRY_AUTH_HTPASSWD_PATH=/opt/htpasswd/htpasswd.conf",
        "--mount",
        f"type=bind,src={htpasswd_dir},dst=/opt/htpasswd",
        "-p",
        f"{port}:5000",
        registry_image,
    ]
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
        yield f"{host_ip}:{port}", username, password
    finally:
        proc.terminate()
        proc.wait()


def test_registry_explicit_creds(registry, dind):
    """
    Test that we can push to registry when given explicit credentials
    """
    registry_host, username, password = registry
    image_name = f"{registry_host}/{secrets.token_hex(8)}:latest"
    r2d = make_r2d(["--image", image_name, "--push", "--no-run", str(HERE)])

    docker_host, cert_dir = dind

    old_environ = os.environ.copy()

    try:
        os.environ["DOCKER_HOST"] = docker_host
        os.environ["DOCKER_CERT_PATH"] = str(cert_dir / "client")
        os.environ["DOCKER_TLS_VERIFY"] = "1"
        os.environ["CONTAINER_ENGINE_REGISTRY_CREDENTIALS"] = json.dumps(
            {
                "registry": f"http://{registry_host}",
                "username": username,
                "password": password,
            }
        )
        r2d.start()

        # CONTAINER_ENGINE_REGISTRY_CREDENTIALS unfortunately doesn't propagate to docker manifest, so
        # let's explicitly set up a docker_config here so we can check if the image exists
        with TemporaryDirectory() as d:
            (Path(d) / "config.json").write_text(
                json.dumps(
                    {
                        "auths": {
                            f"http://{registry_host}": {
                                "auth": b64encode(
                                    f"{username}:{password}".encode()
                                ).decode()
                            }
                        }
                    }
                )
            )
            env = os.environ.copy()
            env["DOCKER_CONFIG"] = d
            proc = subprocess.run(
                ["docker", "manifest", "inspect", "--insecure", image_name], env=env
            )
            assert proc.returncode == 0

        # Validate that we didn't leak our registry creds into existing docker config
        docker_config_path = Path(
            os.environ.get("DOCKER_CONFIG", "~/.docker/config.json")
        ).expanduser()
        if docker_config_path.exists():
            # Just check that our randomly generated password is not in this file
            # Can this cause a conflict? Sure, if there's a different randomly generated password in here
            # that matches our own randomly generated password. But if you're that unlucky, take cover from the asteroid.
            assert password not in docker_config_path.read_text()
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_registry_no_explicit_creds(registry, dind):
    """
    Test that we can push to registry *without* explicit credentials but reading from a DOCKER_CONFIG
    """
    registry_host, username, password = registry
    image_name = f"{registry_host}/{secrets.token_hex(8)}:latest"
    r2d = make_r2d(["--image", image_name, "--push", "--no-run", str(HERE)])

    docker_host, cert_dir = dind

    old_environ = os.environ.copy()

    try:
        os.environ["DOCKER_HOST"] = docker_host
        os.environ["DOCKER_CERT_PATH"] = str(cert_dir / "client")
        os.environ["DOCKER_TLS_VERIFY"] = "1"
        with TemporaryDirectory() as d:
            (Path(d) / "config.json").write_text(
                json.dumps(
                    {
                        "auths": {
                            f"http://{registry_host}": {
                                "auth": b64encode(
                                    f"{username}:{password}".encode()
                                ).decode()
                            }
                        }
                    }
                )
            )
            os.environ["DOCKER_CONFIG"] = d
            r2d.start()

            proc = subprocess.run(
                ["docker", "manifest", "inspect", "--insecure", image_name]
            )
            assert proc.returncode == 0
    finally:
        os.environ.clear()
        os.environ.update(old_environ)
