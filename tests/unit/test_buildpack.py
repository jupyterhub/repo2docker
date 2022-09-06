from os.path import join as pjoin

import pytest
from tempfile import TemporaryDirectory
from repo2docker.buildpacks import LegacyBinderDockerBuildPack, PythonBuildPack
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


@pytest.mark.parametrize("python_version", ["2.6", "3.0", "4.10", "3.99"])
def test_unsupported_python(tmpdir, python_version):
    tmpdir.chdir()
    bp = PythonBuildPack()
    bp._python_version = python_version
    assert bp.python_version == python_version
    with pytest.raises(ValueError):
        bp.render()
