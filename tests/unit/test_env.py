"""
Test that environment variables may be defined
"""
import os
import subprocess
import tempfile
import time
from getpass import getuser


def test_env():
    """
    Validate that you can define environment variables
    """
    ts = str(time.time())
    # There appear to be some odd combinations of default dir that do
    # not work on macOS Catalina with Docker CE 2.2.0.5, so use
    # the current dir -- it'll be deleted immediately

    with tempfile.TemporaryDirectory(dir=os.path.abspath(os.curdir)) as tmpdir:
        username = getuser()
        subprocess.check_call(
            [
                "repo2docker",
                "-v",
                "{}:/home/{}".format(tmpdir, username),
                "-e",
                "FOO={}".format(ts),
                "--env",
                "BAR=baz",
                "--",
                tmpdir,
                "/bin/bash",
                "-c",
                "echo -n $FOO > ts && echo -n $BAR > bar",
            ]
        )

        with open(os.path.join(tmpdir, "ts")) as f:
            assert f.read().strip() == ts
        with open(os.path.join(tmpdir, "bar")) as f:
            assert f.read().strip() == "baz"
