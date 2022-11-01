import os
import subprocess
from tempfile import TemporaryDirectory

import pytest

from repo2docker.contentproviders import Git


def test_clone(repo_with_content):
    """Test simple git clone to a target dir"""
    upstream, sha1 = repo_with_content

    with TemporaryDirectory() as clone_dir:
        spec = {"repo": upstream}
        git_content = Git()
        for _ in git_content.fetch(spec, clone_dir):
            pass
        assert os.path.exists(os.path.join(clone_dir, "test"))

        assert git_content.content_id == sha1[:7]


def test_submodule_clone(repo_with_submodule):
    """Test git clone containing a git submodule."""
    upstream, expected_sha1_upstream, expected_sha1_submod = repo_with_submodule

    # check that checking out a branch where there are no submodule
    # indeed doesn't get any submodule, even though they are in master
    with TemporaryDirectory() as clone_dir2:
        submod_dir = os.path.join(clone_dir2, "submod")  # set by fixture
        spec = {"repo": upstream, "ref": "branch-without-submod"}
        git_content = Git()
        for _ in git_content.fetch(spec, clone_dir2):
            pass

        assert os.path.exists(os.path.join(clone_dir2, "test"))
        assert not os.path.exists(os.path.join(submod_dir, "requirements.txt"))

    with TemporaryDirectory() as clone_dir:
        submod_dir = os.path.join(clone_dir, "submod")  # set by fixture
        spec = {"repo": upstream}
        git_content = Git()
        for _ in git_content.fetch(spec, clone_dir):
            pass
        assert os.path.exists(os.path.join(clone_dir, "test"))
        assert os.path.exists(os.path.join(submod_dir, "requirements.txt"))

        # get current sha1 of submodule
        cmd = ["git", "rev-parse", "HEAD"]
        sha1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=submod_dir)
        submod_sha1 = sha1.stdout.read().decode().strip()

        assert git_content.content_id == expected_sha1_upstream[:7]
        assert submod_sha1[:7] == expected_sha1_submod[:7]


def test_bad_ref(repo_with_content):
    """
    Test trying to checkout a ref that doesn't exist
    """
    upstream, sha1 = repo_with_content
    with TemporaryDirectory() as clone_dir:
        spec = {"repo": upstream, "ref": "does-not-exist"}
        with pytest.raises(ValueError):
            for _ in Git().fetch(spec, clone_dir):
                pass


def test_always_accept():
    # The git content provider should always accept a spec
    assert Git().detect("/tmp/doesnt-exist", ref="1234")
    assert Git().detect("/tmp/doesnt-exist")
    # a path that exists
    assert Git().detect("/etc", ref="1234")
    # a remote URL
    assert Git().detect("https://example.com/path/here")
