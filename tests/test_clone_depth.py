"""
Test that a clone depth of 1 is used and good enough when no refspec is used

Note: the tests don't actually run the container. Building the
container requires a specific repository and commit to be checked out,
and that is the only thing that is tested.

"""
import subprocess
import requests
import time
from repo2docker.app import Repo2Docker


URL = "https://github.com/binderhub-ci-repos/repo2docker-ci-clone-depth"


def test_clone_depth():
    """Test a remote repository, without a refspec"""

    app = Repo2Docker()
    argv = [URL]
    app.initialize(argv)
    app.debug = True
    app.run = False
    app.cleanup_checkout = False
    app.start()  # This just build the image and does not run it.

    # Building the image has already put us in the cloned repository directory
    cmd = ['git', 'rev-parse', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'703322e9c6635ba1835d3b92eafbabeca0042c3e'
    cmd = ['git', 'rev-list', '--count', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'1'
    with open('COMMIT') as fp:
        assert fp.read() == '100\n'


def test_clone_depth_full():
    """Test a remote repository, with a refspec of 'master'"""

    app = Repo2Docker()
    argv = ['--ref', 'master', URL]
    app.initialize(argv)
    app.debug = True
    app.run = False
    app.cleanup_checkout = False
    app.start()  # This just build the image and does not run it.

    # Building the image has already put us in the cloned repository directory
    cmd = ['git', 'rev-parse', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'703322e9c6635ba1835d3b92eafbabeca0042c3e'
    cmd = ['git', 'rev-list', '--count', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'100'
    with open('COMMIT') as fp:
        assert fp.read() == '100\n'


def test_clone_depth_full2():
    """Test a remote repository, with a refspec of the master commit hash"""

    app = Repo2Docker()
    argv = ['--ref', '703322e', URL]

    app.initialize(argv)
    app.debug = True
    app.run = False
    app.cleanup_checkout = False
    app.start()  # This just build the image and does not run it.

    # Building the image has already put us in the cloned repository directory
    cmd = ['git', 'rev-parse', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'703322e9c6635ba1835d3b92eafbabeca0042c3e'
    cmd = ['git', 'rev-list', '--count', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'100'
    with open('COMMIT') as fp:
        assert fp.read() == '100\n'


def test_clone_depth_mid():
    """Test a remote repository, with a refspec of a commit hash halfway"""

    app = Repo2Docker()
    argv = ['--ref', '8bc4f21', URL]

    app.initialize(argv)
    app.debug = True
    app.run = False
    app.cleanup_checkout = False
    app.start()  # This just build the image and does not run it.

    # Building the image has already put us in the cloned repository directory
    cmd = ['git', 'rev-parse', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'8bc4f216856f86f6fc25a788b744b93b87e9ba48'
    cmd = ['git', 'rev-list', '--count', 'HEAD']
    p = subprocess.run(cmd, stdout=subprocess.PIPE)
    assert p.stdout.strip() == b'50'
    with open('COMMIT') as fp:
        assert fp.read() == '50\n'
