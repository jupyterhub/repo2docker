import os
import re
import tempfile
import time

from repo2docker.__main__ import make_r2d


DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dockerfile", "editable")


def test_editable(run_repo2docker):
    """Run a local repository in edit mode. Verify a new file has been
    created afterwards"""
    newfile = os.path.join(DIR, "newfile")
    try:
        # If the file didn't get properly cleaned up last time, we
        # need to do that now
        os.remove(newfile)
    except FileNotFoundError:
        pass
    argv = ["--editable", DIR, "/usr/local/bin/change.sh"]
    run_repo2docker(argv)
    try:
        with open(newfile) as fp:
            contents = fp.read()
        assert contents == "new contents\n"
    finally:
        os.remove(newfile)


def test_editable_by_host():
    """Test whether a new file created by the host environment, is
    detected in the container"""

    app = make_r2d(["--editable", DIR])
    app.initialize()
    app.build()
    container = app.start_container()

    # give the container a chance to start
    while container.status != "running":
        time.sleep(1)

    try:
        with tempfile.NamedTemporaryFile(dir=DIR, prefix="testfile", suffix=".txt"):
            status, output = container._c.exec_run(
                ["sh", "-c", "ls testfile????????.txt"]
            )
            assert status == 0
            assert re.match(br"^testfile\w{8}\.txt\n$", output) is not None
        # After exiting the with block the file should stop existing
        # in the container as well as locally
        status, output = container._c.exec_run(["sh", "-c", "ls testfile????????.txt"])
        assert status == 2
        assert re.match(br"^testfile\w{8}\.txt\n$", output) is None

    finally:
        # stop the container, we don't care how it stops or
        # what the exit code is.
        container.stop(timeout=1)
        container.reload()
        assert container.status == "exited", container.status
        container.remove()
