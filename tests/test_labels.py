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
    if ref is not None:
        argv = ['--ref', ref, str(tmpdir)]
    else:
        argv = [str(tmpdir)]
    app.initialize(argv)
    app.debug = True
    app.run = False
    app.start()  # This just build the image and does not run it.
    container = app.start_container()
    expected_labels = {
        'repo2docker.ref': str(ref),
        'repo2docker.repo': str(tmpdir),
        'repo2docker.version': __version__,
    }

    # wait a bit for the container to be ready
    # give the container a chance to start
    time.sleep(1)

    try:
        assert container.labels == expected_labels
    finally:
        # stop the container
        container.stop()
        app.wait_for_container(container)
