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

    See https://gist.github.com/hwine/9f5b02c894427324fafcf12f772b27b7
    for how docker handles its -e & --env argument values
    """
    ts = str(time.time())
    # There appear to be some odd combinations of default dir that do
    # not work on macOS Catalina with Docker CE 2.2.0.5, so use
    # the current dir -- it'll be deleted immediately

    with tempfile.TemporaryDirectory(dir=os.path.abspath(os.curdir)) as tmpdir:
        username = getuser()
        os.environ["SPAM"] = "eggs"
        os.environ["SPAM_2"] = "ham"
        result = subprocess.run(
            [
                "repo2docker",
                # 'key=value' are exported as is in docker
                "-e",
                "FOO={}".format(ts),
                "--env",
                "BAR=baz",
                # 'key' is exported with the currently exported value
                "--env",
                "SPAM",
                # 'key' is not exported if it is not exported.
                "-e",
                "NO_SPAM",
                # 'key=' is exported in docker with an empty string as
                # value
                "--env",
                "SPAM_2=",
                # "--",
                tmpdir,
                "/bin/bash",
                "-c",
                # Docker exports all passed env variables, so we can
                # just look at exported variables.
                "export; sleep 1",
                # "export; echo TIMDONE",
                # "export",
            ],
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    assert result.returncode == 0

    # all docker output is returned by repo2docker on stderr
    # extract just the declare for better failure message formatting
    # stdout should be empty
    assert not result.stdout

    print(result.stderr.split("\n"))
    # assert False

    # stderr should contain lines of output
    declares = [x for x in result.stderr.split("\n") if x.startswith("declare")]
    assert 'declare -x FOO="{}"'.format(ts) in declares
    assert 'declare -x BAR="baz"' in declares
    assert 'declare -x SPAM="eggs"' in declares
    assert "declare -x NO_SPAM" not in declares
    assert 'declare -x SPAM_2=""' in declares
