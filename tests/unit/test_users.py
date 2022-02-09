"""
Test that User name and ID mapping works
"""
import os
import subprocess
import tempfile
import time
from getpass import getuser
from unittest import mock

from repo2docker import Repo2Docker


def test_automatic_username_deduction():
    # check we pickup the right username
    with mock.patch("os.environ") as mock_env:
        expected = "someusername"
        mock_env.get.return_value = expected

        r2d = Repo2Docker()
        assert r2d.user_name == expected


def test_user():
    """
    Validate user id and name setting
    """
    ts = str(time.time())
    # FIXME: Use arbitrary login here, We need it now since we wanna put things to volume.
    username = getuser()
    userid = str(os.geteuid())
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = os.path.realpath(tmpdir)
        subprocess.check_call(
            [
                "repo2docker",
                "-v",
                "{}:/home/{}".format(tmpdir, username),
                "--user-id",
                userid,
                "--user-name",
                username,
                tmpdir,
                "--",
                "/bin/bash",
                "-c",
                "id -u > id && id -g > grp && pwd > pwd && whoami > name && echo -n $USER > env_user".format(
                    ts
                ),
            ]
        )

        with open(os.path.join(tmpdir, "id")) as f:
            assert f.read().strip() == userid
        with open(os.path.join(tmpdir, "pwd")) as f:
            assert f.read().strip() == "/home/{}".format(username)
        with open(os.path.join(tmpdir, "name")) as f:
            assert f.read().strip() == username
        with open(os.path.join(tmpdir, "name")) as f:
            assert f.read().strip() == username
        # When group-id NOT specified, group id in container is user id
        with open(os.path.join(tmpdir, "grp")) as f:
            assert f.read().strip() == userid


def test_user_groups():
    """
    Validate user id and name setting
    """
    ts = str(time.time())
    # FIXME: Use arbitrary login here, We need it now since we wanna put things to volume.
    username = getuser()
    userid = str(os.geteuid())
    groupid = str(os.geteuid() + 1)
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = os.path.realpath(tmpdir)
        subprocess.check_call(
            [
                "repo2docker",
                "-v",
                "{}:/home/{}".format(tmpdir, username),
                "--user-id",
                userid,
                "--user-name",
                username,
                "--group-id",
                groupid,
                tmpdir,
                "--",
                "/bin/bash",
                "-c",
                "id -u > id && id -g > grp && stat --format %u:%g grp > id_grp && pwd > pwd && whoami > name && echo -n $USER > env_user".format(
                    ts
                ),
            ]
        )

        with open(os.path.join(tmpdir, "id")) as f:
            assert f.read().strip() == userid
        with open(os.path.join(tmpdir, "pwd")) as f:
            assert f.read().strip() == "/home/{}".format(username)
        with open(os.path.join(tmpdir, "name")) as f:
            assert f.read().strip() == username
        with open(os.path.join(tmpdir, "name")) as f:
            assert f.read().strip() == username
        # When group-id specified, group id in container is same as specified
        with open(os.path.join(tmpdir, "grp")) as f:
            assert f.read().strip() == groupid
        with open(os.path.join(tmpdir, "id_grp")) as f:
            assert f.read().strip() == userid + ":" + groupid
