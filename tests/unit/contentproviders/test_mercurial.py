from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import sys

import pytest

from repo2docker.contentproviders import Mercurial


skipif_py35 = pytest.mark.skipif(sys.version_info < (3, 6), reason="requires python3.6")


def _add_content_to_hg(repo_dir):
    """Add content to file 'test' in hg repository and commit."""
    # use append mode so this can be called multiple times
    with open(Path(repo_dir) / "test", "a") as f:
        f.write("Hello")

    subprocess.check_call(["hg", "add", "test"], cwd=repo_dir)
    subprocess.check_call(["hg", "commit", "-m", "Test commit"], cwd=repo_dir)


def _get_node_id(repo_dir):
    """Get repository's current commit node ID (currently SHA1)."""
    node_id = subprocess.Popen(
        ["hg", "identify", "-i"], stdout=subprocess.PIPE, cwd=repo_dir
    )
    return node_id.stdout.read().decode().strip()


@pytest.fixture()
def hg_repo():
    """
    Make a dummy hg repo in which user can perform hg operations

    Should be used as a contextmanager, it will delete directory when done
    """
    with TemporaryDirectory() as hgdir:
        subprocess.check_call(["hg", "init"], cwd=hgdir)
        yield hgdir


@pytest.fixture()
def hg_repo_with_content(hg_repo):
    """Create a hg repository with content"""
    _add_content_to_hg(hg_repo)
    node_id = _get_node_id(hg_repo)

    yield hg_repo, node_id


@skipif_py35
def test_detect_mercurial(hg_repo_with_content, repo_with_content):
    mercurial = Mercurial()
    assert mercurial.detect("this-is-not-a-directory") is None
    assert mercurial.detect("https://github.com/jupyterhub/repo2docker") is None

    git_repo = repo_with_content[0]
    assert mercurial.detect(git_repo) is None

    hg_repo = hg_repo_with_content[0]
    assert mercurial.detect(hg_repo) == {"repo": hg_repo, "ref": None}


@skipif_py35
def test_clone(hg_repo_with_content):
    """Test simple hg clone to a target dir"""
    upstream, node_id = hg_repo_with_content

    with TemporaryDirectory() as clone_dir:
        spec = {"repo": upstream}
        mercurial = Mercurial()
        for _ in mercurial.fetch(spec, clone_dir):
            pass
        assert (Path(clone_dir) / "test").exists()

        assert mercurial.content_id == node_id


@skipif_py35
def test_bad_ref(hg_repo_with_content):
    """
    Test trying to checkout a ref that doesn't exist
    """
    upstream, node_id = hg_repo_with_content
    with TemporaryDirectory() as clone_dir:
        spec = {"repo": upstream, "ref": "does-not-exist"}
        with pytest.raises(ValueError):
            for _ in Mercurial().fetch(spec, clone_dir):
                pass
