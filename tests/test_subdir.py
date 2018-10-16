"""
Test if the subdirectory is correctly navigated to
"""
import logging

import pytest
from repo2docker.app import Repo2Docker

TEST_REPO = "https://github.com/binderhub-ci-repos/repo2docker-subdir-support"


def test_subdir(run_repo2docker):
    # Build from a subdirectory
    # if subdir support is broken this will fail as the instructions in the
    # root of the test repo are invalid
    argv = ['--subdir', 'a directory', TEST_REPO]
    run_repo2docker(argv)


def test_subdir_invalid(caplog):
    # test an error is raised when requesting a non existent subdir
    caplog.set_level(logging.INFO)

    app = Repo2Docker()
    argv = ['--subdir', 'invalid-sub-dir', TEST_REPO]
    app.initialize(argv)
    app.debug = True
    # no build implies no run
    app.build = False
    with pytest.raises(SystemExit) as excinfo:
        app.start()  # Just build the image and do not run it.

    # The build should fail
    assert excinfo.value.code == 1

    # Can't get this to record the logs?
    assert caplog.text == "Subdirectory tests/conda/invalid does not exist"
