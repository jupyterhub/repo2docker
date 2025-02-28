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
