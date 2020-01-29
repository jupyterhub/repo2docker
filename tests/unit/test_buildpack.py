from os.path import join as pjoin

import pytest
from tempfile import TemporaryDirectory
from repo2docker.buildpacks import LegacyBinderDockerBuildPack
from repo2docker.utils import chdir


def test_legacy_raises():
    # check legacy buildpack raises on a repo that triggers it
    with TemporaryDirectory() as repodir:
        with open(pjoin(repodir, "Dockerfile"), "w") as d:
            d.write("FROM andrewosh/binder-base")

        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack()
            with pytest.raises(RuntimeError):
                bp.detect()


def test_legacy_doesnt_detect():
    # check legacy buildpack doesn't trigger
    with TemporaryDirectory() as repodir:
        with open(pjoin(repodir, "Dockerfile"), "w") as d:
            d.write("FROM andrewosh/some-image")

        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack()
            assert not bp.detect()


def test_legacy_on_repo_without_dockerfile():
    # check legacy buildpack doesn't trigger on a repo w/o Dockerfile
    with TemporaryDirectory() as repodir:
        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack()
            assert not bp.detect()
