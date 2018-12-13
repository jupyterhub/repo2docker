"""
Test if labels are supplied correctly to the container
"""
import time
from unittest.mock import Mock
from repo2docker.app import Repo2Docker
from repo2docker.buildpacks import BuildPack
from repo2docker import __version__
import pytest


def test_buildpack_labels_rendered():
    bp = BuildPack()
    assert 'LABEL' not in bp.render()
    bp.labels['first_label'] = 'firstlabel'
    assert 'LABEL first_label="firstlabel"\n' in bp.render()
    bp.labels['second_label'] = 'anotherlabel'
    assert 'LABEL second_label="anotherlabel"\n' in bp.render()


@pytest.mark.parametrize('ref', ['some-branch', None])
def test_labels(ref, tmpdir):
    repo = str(tmpdir)
    if ref is not None:
        argv = ['--ref', ref, repo]
    else:
        argv = [repo]

    app = Repo2Docker()
    # Add mock BuildPack to app
    mock_buildpack = Mock()
    mock_buildpack.return_value.labels = {}
    app.buildpacks = [mock_buildpack]

    app.initialize(argv)
    app.build = False
    app.run = False
    app.start()
    expected_labels = {
        'repo2docker.ref': ref,
        'repo2docker.repo': repo,
        'repo2docker.version': __version__,
    }

    assert mock_buildpack().labels == expected_labels
