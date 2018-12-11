"""
Tests for repo2docker/utils.py
"""
import os
from tempfile import TemporaryDirectory
from repo2docker import utils
import pytest
import subprocess


def test_capture_cmd_no_capture_success():
    # This should succeed
    for line in utils.execute_cmd([
        '/bin/bash', '-c', 'echo test'
    ]):
        pass

def test_capture_cmd_no_capture_fail():
    with pytest.raises(subprocess.CalledProcessError):
        for line in utils.execute_cmd([
            '/bin/bash', '-c', 'e '
        ]):
            pass


def test_capture_cmd_capture_success():
    # This should succeed
    for line in utils.execute_cmd([
        '/bin/bash', '-c', 'echo test'
    ], capture=True):
        assert line == 'test\n'


def test_capture_cmd_capture_fail():
    with pytest.raises(subprocess.CalledProcessError):
        for line in utils.execute_cmd([
            '/bin/bash', '-c', 'echo test; exit 1 '
        ], capture=True):
            assert line == 'test\n'


def test_chdir():
    with TemporaryDirectory() as d:
        cur_cwd = os.getcwd()
        with utils.chdir(d):
            assert os.getcwd() == d
        assert os.getcwd() == cur_cwd
