"""
Test that a clone depth of 1 is used when HEAD or no refspec is used

Note: the tests don't actually run the container. Building the
container requires a specific repository and commit to be checked out,
and that is the only thing that is tested.

"""
import os
import subprocess

from tempfile import TemporaryDirectory

from repo2docker.app import Repo2Docker


URL = "https://github.com/binderhub-ci-repos/repo2docker-ci-clone-depth"


def test_clone_depth():
    """Test a remote repository, without a refspec"""

    with TemporaryDirectory() as d:
        app = Repo2Docker(
            repo=URL,
            dry_run=True,
            run=False,
            # turn off automatic clean up of the checkout so we can inspect it
            # we also set the work directory explicitly so we know where to look
            cleanup_checkout=False,
            git_workdir=d,
        )
        app.initialize()
        app.start()

        cmd = ["git", "rev-parse", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"703322e9c6635ba1835d3b92eafbabeca0042c3e"
        cmd = ["git", "rev-list", "--count", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"1"
        with open(os.path.join(d, "COMMIT")) as fp:
            assert fp.read() == "100\n"


def test_clone_depth_head():
    """Test a remote repository, with a refspec of 'HEAD'"""

    with TemporaryDirectory() as d:
        app = Repo2Docker(
            repo=URL,
            ref="HEAD",
            dry_run=True,
            run=False,
            # turn off automatic clean up of the checkout so we can inspect it
            # we also set the work directory explicitly so we know where to look
            cleanup_checkout=False,
            git_workdir=d,
        )
        app.initialize()
        app.start()

        cmd = ["git", "rev-parse", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"703322e9c6635ba1835d3b92eafbabeca0042c3e"
        cmd = ["git", "rev-list", "--count", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"1"
        with open(os.path.join(d, "COMMIT")) as fp:
            assert fp.read() == "100\n"


def test_clone_depth_full():
    """Test a remote repository, with a refspec of 'master'"""

    with TemporaryDirectory() as d:
        app = Repo2Docker(
            repo=URL,
            ref="master",
            dry_run=True,
            run=False,
            # turn off automatic clean up of the checkout so we can inspect it
            # we also set the work directory explicitly so we know where to look
            cleanup_checkout=False,
            git_workdir=d,
        )
        app.initialize()
        app.start()

        # Building the image has already put us in the cloned repository directory
        cmd = ["git", "rev-parse", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"703322e9c6635ba1835d3b92eafbabeca0042c3e"
        cmd = ["git", "rev-list", "--count", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"100"
        with open(os.path.join(d, "COMMIT")) as fp:
            assert fp.read() == "100\n"


def test_clone_depth_full2():
    """Test a remote repository, with a refspec of the master commit hash"""

    with TemporaryDirectory() as d:
        app = Repo2Docker(
            repo=URL,
            ref="703322e",
            dry_run=True,
            run=False,
            # turn off automatic clean up of the checkout so we can inspect it
            # we also set the work directory explicitly so we know where to look
            cleanup_checkout=False,
            git_workdir=d,
        )
        app.initialize()
        app.start()

        # Building the image has already put us in the cloned repository directory
        cmd = ["git", "rev-parse", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"703322e9c6635ba1835d3b92eafbabeca0042c3e"
        cmd = ["git", "rev-list", "--count", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"100"
        with open(os.path.join(d, "COMMIT")) as fp:
            assert fp.read() == "100\n"


def test_clone_depth_mid():
    """Test a remote repository, with a refspec of a commit hash halfway"""

    with TemporaryDirectory() as d:
        app = Repo2Docker(
            repo=URL,
            ref="8bc4f21",
            dry_run=True,
            run=False,
            # turn off automatic clean up of the checkout so we can inspect it
            # we also set the work directory explicitly so we know where to look
            cleanup_checkout=False,
            git_workdir=d,
        )
        app.initialize()
        app.start()

        # Building the image has already put us in the cloned repository directory
        cmd = ["git", "rev-parse", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"8bc4f216856f86f6fc25a788b744b93b87e9ba48"
        cmd = ["git", "rev-list", "--count", "HEAD"]
        p = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=d)
        assert p.stdout.strip() == b"50"
        with open(os.path.join(d, "COMMIT")) as fp:
            assert fp.read() == "50\n"
