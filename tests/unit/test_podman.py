"""Tests for podman client"""

import pytest
import os
import re
from repo2docker.podman import Container, PodmanClient
from subprocess import CalledProcessError
from time import sleep


def test_run_attach():
    client = PodmanClient()
    out = client.containers.run("busybox", command=["id", "-un"], remove=True)
    # If image was pulled the progress logs will also be present
    # assert len(out) == 1
    assert out[-1].strip() == "root", out


def test_run_detach_nostream():
    client = PodmanClient()
    c = client.containers.run("busybox", command=["id", "-un"], detach=True)
    assert isinstance(c, Container)
    assert re.match("^[0-9a-f]{64}$", c.id)
    sleep(1)
    c.reload()
    assert c.status == "exited"
    out = c.logs()
    assert out.strip() == "root"
    c.remove()
    with pytest.raises(CalledProcessError):
        c.reload()


# @pytest.mark.parametrize('sleep', [0, 5])
def test_run_detach_stream_live():
    client = PodmanClient()
    c = client.containers.run(
        "busybox", command=["sh", "-c", "sleep 5; id -un"], detach=True
    )
    assert isinstance(c, Container)
    assert re.match("^[0-9a-f]{64}$", c.id)
    sleep(1)
    c.reload()
    assert c.status == "running"
    out = "\n".join(line.decode("utf-8") for line in c.logs(stream=True))
    assert out.strip() == "root"
    c.remove()
    with pytest.raises(CalledProcessError):
        c.reload()


def test_run_detach_stream_exited():
    client = PodmanClient()
    c = client.containers.run("busybox", command=["id", "-un"], detach=True)
    assert isinstance(c, Container)
    assert re.match("^[0-9a-f]{64}$", c.id)
    sleep(1)
    c.reload()
    assert c.status == "exited"
    out = "\n".join(line.decode("utf-8") for line in c.logs(stream=True))
    assert out.strip() == "root"
    c.remove()
    with pytest.raises(CalledProcessError):
        c.reload()
