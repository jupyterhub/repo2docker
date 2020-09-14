from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import os
from distutils.util import strtobool

import pytest

from repo2docker.contentproviders import Mercurial
from repo2docker.contentproviders.mercurial import args_enabling_topic

SKIP_HG = strtobool(os.environ.get("REPO2DOCKER_SKIP_HG_TESTS", "False"))

skip_if_no_hg_tests = pytest.mark.skipif(
    SKIP_HG,
    reason="REPO2DOCKER_SKIP_HG_TESTS",
)


@skip_if_no_hg_tests
def test_if_mercurial_is_available():
    """
    To skip the tests related to Mercurial repositories (to avoid to install
    Mercurial and hg-evolve), one can use the environment variable
    REPO2DOCKER_SKIP_HG_TESTS.
    """
    subprocess.check_output(["hg", "version"])


@skip_if_no_hg_tests
def test_if_topic_is_available():
    """Check that the topic extension can be enabled"""
    output = subprocess.getoutput("hg version -v --config extensions.topic=")
    assert "failed to import extension topic" not in output


def _add_content_to_hg(repo_dir):
    """Add content to file 'test' in hg repository and commit."""
    # use append mode so this can be called multiple times
    with open(Path(repo_dir) / "test", "a") as f:
        f.write("Hello")

    def check_call(command):
        subprocess.check_call(command + args_enabling_topic, cwd=repo_dir)

    check_call(["hg", "add", "test"])
    check_call(["hg", "commit", "-m", "Test commit"])
    check_call(["hg", "topic", "test-topic"])
    check_call(["hg", "commit", "-m", "Test commit in topic test-topic"])
    check_call(["hg", "up", "default"])


def _get_node_id(repo_dir):
    """Get repository's current commit node ID (currently SHA1)."""
    node_id = subprocess.Popen(
        ["hg", "identify", "-i"] + args_enabling_topic,
        stdout=subprocess.PIPE,
        cwd=repo_dir,
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


@skip_if_no_hg_tests
def test_detect_mercurial(hg_repo_with_content, repo_with_content):
    mercurial = Mercurial()
    assert mercurial.detect("this-is-not-a-directory") is None
    assert mercurial.detect("https://github.com/jupyterhub/repo2docker") is None

    git_repo = repo_with_content[0]
    assert mercurial.detect(git_repo) is None

    hg_repo = hg_repo_with_content[0]
    assert mercurial.detect(hg_repo) == {"repo": hg_repo, "ref": None}


@skip_if_no_hg_tests
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


@skip_if_no_hg_tests
def test_bad_ref(hg_repo_with_content):
    """
    Test trying to update to a ref that doesn't exist
    """
    upstream, node_id = hg_repo_with_content
    with TemporaryDirectory() as clone_dir:
        spec = {"repo": upstream, "ref": "does-not-exist"}
        with pytest.raises(ValueError):
            for _ in Mercurial().fetch(spec, clone_dir):
                pass


@skip_if_no_hg_tests
def test_ref_topic(hg_repo_with_content):
    """
    Test trying to update to a topic

    To skip this test (to avoid to install Mercurial and hg-evolve), one can
    use the environment variable REPO2DOCKER_SKIP_HG_TESTS.

    """
    upstream, node_id = hg_repo_with_content
    node_id = subprocess.Popen(
        ["hg", "identify", "-i", "-r", "topic(test-topic)"] + args_enabling_topic,
        stdout=subprocess.PIPE,
        cwd=upstream,
    )
    node_id = node_id.stdout.read().decode().strip()

    with TemporaryDirectory() as clone_dir:
        spec = {"repo": upstream, "ref": "test-topic"}
        mercurial = Mercurial()
        for _ in mercurial.fetch(spec, clone_dir):
            pass
        assert (Path(clone_dir) / "test").exists()

        assert mercurial.content_id == node_id
