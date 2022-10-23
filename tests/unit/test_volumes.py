"""
Test that volume mounts work when running
"""

import os
import subprocess
import tempfile
import time
from getpass import getuser


def test_volume_abspath():
    """
    Validate that you can bind mount a volume onto an absolute dir & write to it
    """
    ts = str(time.time())
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = os.path.realpath(tmpdir)

        username = getuser()
        subprocess.check_call(
            [
                "repo2docker",
                "-v",
                f"{tmpdir}:/home/{username}",
                "--user-id",
                str(os.geteuid()),
                "--user-name",
                username,
                tmpdir,
                "--",
                "/bin/bash",
                "-c",
                f"echo -n {ts} > ts",
            ]
        )

        with open(os.path.join(tmpdir, "ts")) as f:
            assert f.read() == ts


def test_volume_relpath():
    """
    Validate that you can bind mount a volume onto an relative path & write to it
    """
    curdir = os.getcwd()
    try:
        ts = str(time.time())
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            subprocess.check_call(
                [
                    "repo2docker",
                    "-v",
                    ".:.",
                    "--user-id",
                    str(os.geteuid()),
                    "--user-name",
                    getuser(),
                    tmpdir,
                    "--",
                    "/bin/bash",
                    "-c",
                    f"echo -n {ts} > ts",
                ]
            )

            with open(os.path.join(tmpdir, "ts")) as f:
                assert f.read() == ts
    finally:
        os.chdir(curdir)
