"""Tests for docker bits"""

import os
from subprocess import check_output
from unittest.mock import Mock, patch

from repo2docker.docker import DockerEngine

repo_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)


def test_git_credential_env():
    credential_env = "username=abc\npassword=def"
    out = (
        check_output(
            os.path.join(repo_root, "docker", "git-credential-env"),
            env={"GIT_CREDENTIAL_ENV": credential_env},
        )
        .decode()
        .strip()
    )
    assert out == credential_env


class MockDockerEngine(DockerEngine):
    def __init__(self, *args, **kwargs):
        self._apiclient = Mock()


def test_docker_push_no_credentials():
    engine = MockDockerEngine()

    engine.push("image")

    assert len(engine._apiclient.method_calls) == 1
    engine._apiclient.push.assert_called_once_with("image", stream=True)


def test_docker_push_dict_credentials():
    engine = MockDockerEngine()
    engine.registry_credentials = {"username": "abc", "password": "def"}

    engine.push("image")

    assert len(engine._apiclient.method_calls) == 2
    engine._apiclient.login.assert_called_once_with(username="abc", password="def")
    engine._apiclient.push.assert_called_once_with("image", stream=True)


def test_docker_push_env_credentials():
    engine = MockDockerEngine()
    with patch.dict(
        "os.environ",
        {
            "CONTAINER_ENGINE_REGISTRY_CREDENTIALS": '{"username": "abc", "password": "def"}'
        },
    ):
        engine.push("image")

    assert len(engine._apiclient.method_calls) == 2
    engine._apiclient.login.assert_called_once_with(username="abc", password="def")
    engine._apiclient.push.assert_called_once_with("image", stream=True)
