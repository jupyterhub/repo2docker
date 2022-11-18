#!/usr/bin/env python
import os
import sys


def test_sys_version():
    """The default python version should be 3.10"""
    assert sys.version_info[:2] == (3, 10)


def test_there():
    """there is to be installed via postBuild"""
    import there


def test_conda_activated():
    assert os.environ.get("CONDA_PREFIX") == os.environ["NB_PYTHON_PREFIX"], dict(
        os.environ
    )
