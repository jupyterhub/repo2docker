#!/usr/bin/env python
import os
import sys


def test_sys_prefix():
    # verify that pytest was installed in the notebook env
    assert sys.prefix == os.environ["KERNEL_PYTHON_PREFIX"]


def test_there():
    # verify that there was installed in the notebook env
    import there
