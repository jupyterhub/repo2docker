"""
Test if labels are supplied correctly to the container
"""
import time
from repo2docker.app import Repo2Docker
from repo2docker import __version__
import pytest


@pytest.mark.parametrize('ref', ['some-branch', None])
def test_labels(ref, tmpdir):
    app = Repo2Docker()
    repo = str(tmpdir)
    if ref is not None:
        argv = ['--ref', ref, repo]
    else:
        argv = [repo]
    app.initialize(argv)
    app.build = False
    app.run = False
    app.start()
    labels = app._picked_buildpack.labels
    expected_labels = {
        'repo2docker.ref': ref,
        'repo2docker.repo': repo,
        'repo2docker.version': __version__,
    }

    assert labels == expected_labels
