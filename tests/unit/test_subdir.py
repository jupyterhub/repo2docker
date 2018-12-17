"""
Test if the subdirectory is correctly navigated to
"""
import os
import logging

import pytest
from repo2docker.app import Repo2Docker

TEST_REPO = "https://github.com/binderhub-ci-repos/repo2docker-subdir-support"


def test_subdir(run_repo2docker):
    # Build from a subdirectory
    # if subdir support is broken this will fail as the instructions in the
    # root of the test repo are invalid
    cwd = os.getcwd()

    argv = ['--subdir', 'a directory', TEST_REPO]
    run_repo2docker(argv)

    # check that we restored the current working directory
    assert cwd == os.getcwd(), "We should be back in %s" % cwd


def test_subdir_invalid(caplog):
    # test an error is raised when requesting a non existent subdir
    #caplog.set_level(logging.INFO, logger='Repo2Docker')

    app = Repo2Docker(
        repo=TEST_REPO,
        subdir='invalid-sub-dir',
    )
    app.initialize()
    with pytest.raises(FileNotFoundError):
        app.build()  # Just build the image and do not run it.
