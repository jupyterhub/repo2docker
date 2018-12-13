"""
Test argument parsing and r2d construction
"""
import os
import pytest
import logging
from repo2docker.__main__ import make_r2d
from repo2docker import __version__
from contextlib import redirect_stdout
import io

def test_version():
    """
    Test passing '--version' to repo2docker
    """
    stdout = io.StringIO()
    with redirect_stdout(stdout):
        with pytest.raises(SystemExit):
            make_r2d(['--version'])
    assert stdout.getvalue().strip() == __version__

def test_simple():
    """
    Test simplest possible invocation to r2d
    """
    r2d = make_r2d(['.'])
    assert r2d.repo == '.'

def test_editable():
    """
    Test --editable behavior
    """
    r2d = make_r2d(['--editable', '.'])
    assert r2d.repo == '.'
    assert r2d.volumes[os.getcwd()] == '.'

def test_dry_run():
    """
    Test passing --no-build implies --no-run and lack of --push
    """
    r2d = make_r2d(['--no-build', '.'])
    assert r2d.dry_run
    assert not r2d.run
    assert not r2d.push

def test_run_required():
    """
    Test all the things that should fail if we pass in --no-run
    """
    # Can't use volumes without running
    with pytest.raises(SystemExit):
        make_r2d(['--no-run', '--editable', '.'])

    # Can't publish all ports without running
    with pytest.raises(SystemExit):
        make_r2d(['--no-run', '-P', '.'])

    # Can't publish any ports without running
    with pytest.raises(SystemExit):
        make_r2d(['--no-run', '-p', '8000:8000', '.'])

    # Can't publish any ports while running if we don't specify a command explicitly
    with pytest.raises(SystemExit):
        make_r2d(['-p', '8000:8000', '.'])