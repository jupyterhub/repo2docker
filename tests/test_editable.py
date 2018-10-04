import pytest
import os
import time
from conftest import make_test_func


DIR = os.path.join(os.path.dirname(__file__), 'dockerfile', 'editable')


@pytest.fixture(scope="module")
def run_repo2docker():
    def run_test(args):
        return make_test_func(args)()
    return run_test


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
