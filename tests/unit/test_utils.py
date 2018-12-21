"""
Tests for repo2docker/utils.py
"""
import traitlets
import os
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


def test_chdir(tmpdir):
    d = str(tmpdir.mkdir('cwd'))
    cur_cwd = os.getcwd()
    with utils.chdir(d):
        assert os.getcwd() == d
    assert os.getcwd() == cur_cwd


def test_byte_spec_validation():
    bs = utils.ByteSpecification()

    assert bs.validate(None, 1) == 1
    assert bs.validate(None, 1.0) == 1.0

    assert bs.validate(None, '1K') == 1024
    assert bs.validate(None, '1M') == 1024 * 1024
    assert bs.validate(None, '1G') == 1024 * 1024 * 1024
    assert bs.validate(None, '1T') == 1024 * 1024 * 1024 * 1024

    with pytest.raises(traitlets.TraitError):
        bs.validate(None, 'NK')

    with pytest.raises(traitlets.TraitError):
        bs.validate(None, '1m')


@pytest.mark.parametrize("input,expected", [
    (["8888:8888"], {'8888/tcp': '8888'}),
    (["8888:4321"], {'4321/tcp': '8888'}),
    (["8888:4321/udp"], {'4321/udp': '8888'}),
    (["8888:4321/udp", "8888:4321/tcp"], {'4321/udp': '8888',
                                          '4321/tcp': '8888'}),
    (['127.0.0.1:80:8000'], {'8000/tcp': ('127.0.0.1', '80')}),
    (["8888:4321", "1234:12345"], {'4321/tcp': '8888', '12345/tcp': '1234'}),
])
def test_valid_port_mapping(input, expected):
    actual = utils.validate_and_generate_port_mapping(input)
    assert actual == expected
