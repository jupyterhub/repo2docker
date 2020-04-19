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
    with tempfile.TemporaryDirectory() as tmpdir:
        username = getuser()
        os.environ["SPAM"] = "eggs"
        result = subprocess.run(
            [
                "repo2docker",
                "-e",
                "FOO={}".format(ts),
                "--env",
                "BAR=baz",
                "--env",
                "SPAM",
                "--",
                tmpdir,
                "/bin/bash",
                "-c",
                # Docker exports all passed env variables, so we can
                # just look at that output
                "export",
            ],
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    assert result.returncode == 0
    # all docker output is returned by repo2docker on stderr
    # extract just the declare for better failure message formatting
    declares = [x for x in result.stderr.split("\n") if x.startswith("declare")]
    assert 'declare -x FOO="{}"'.format(ts) in declares
    assert 'declare -x BAR="baz"' in declares
    assert 'declare -x SPAM="eggs"' in declares
