import os
import re
import tempfile
import time

from repo2docker.app import Repo2Docker
from repo2docker.__main__ import make_r2d

from conftest import make_test_func

DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dockerfile', 'editable')


def test_editable(run_repo2docker):
    """Run a local repository in edit mode. Verify a new file has been
    created afterwards"""
    newfile = os.path.join(DIR, 'newfile')
    try:
        # If the file didn't get properly cleaned up last time, we
        # need to do that now
        os.remove(newfile)
    except FileNotFoundError:
        pass
    argv = ['--editable', DIR, '/usr/local/bin/change.sh']
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

    app = make_r2d(['--editable', DIR])
    app.initialize()
    app.build()
    container = app.start_container()
    # give the container a chance to start
    time.sleep(1)
    try:
        with tempfile.NamedTemporaryFile(dir=DIR, prefix='testfile', suffix='.txt'):
            status, output = container.exec_run(['sh', '-c', 'ls testfile????????.txt'])
            assert status == 0
            assert re.match(br'^testfile\w{8}\.txt\n$', output) is not None
        # File should be removed in the container as well
        status, output = container.exec_run(['sh', '-c', 'ls testfile????????.txt'])
        assert status != 1
        assert re.match(br'^testfile\w{8}\.txt\n$', output) is None

    finally:
        # stop the container
        container.stop()
        app.wait_for_container(container)
