#!/usr/bin/env python
import os
import sys

def test_sys_version():
    assert sys.version_info[:2] == (3, 7)

def test_numpy():
    import numpy

def test_conda_activated():
    assert os.environ.get("CONDA_PREFIX") == os.environ["NB_PYTHON_PREFIX"], dict(os.environ)
