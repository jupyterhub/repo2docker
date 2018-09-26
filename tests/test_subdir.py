"""
Test if the explict hostname is supplied correctly to the container
"""
import logging
from os.path import abspath, dirname

import pytest
from repo2docker.app import Repo2Docker
from tests.conftest import make_test_func

repo_path = dirname(dirname(abspath(__file__)))

def test_subdir():
    argv = ['--subdir', 'tests/conda/simple', repo_path]
    make_test_func(argv)()

def test_subdir_invalid(caplog):
    caplog.set_level(logging.INFO, logger='Repo2Docker')

    app = Repo2Docker()
    argv = ['--subdir', 'tests/conda/invalid', repo_path]
    app.initialize(argv)
    app.debug = True
    app.run = False
    with pytest.raises(SystemExit):
        app.start()  # Just build the image and do not run it.

    # Can't get this to record the logs?
    # assert caplog.text == "Subdirectory tests/conda/invalid does not exist"
