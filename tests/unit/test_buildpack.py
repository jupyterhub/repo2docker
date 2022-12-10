from os.path import join as pjoin
from tempfile import TemporaryDirectory

import pytest

from repo2docker.buildpacks import LegacyBinderDockerBuildPack, PythonBuildPack
from repo2docker.utils import chdir


def test_legacy_raises(base_image):
    # check legacy buildpack raises on a repo that triggers it
    with TemporaryDirectory() as repodir:
        with open(pjoin(repodir, "Dockerfile"), "w") as d:
            d.write("FROM andrewosh/binder-base")

        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack(base_image)
            with pytest.raises(RuntimeError):
                bp.detect()


def test_legacy_doesnt_detect(base_image):
    # check legacy buildpack doesn't trigger
    with TemporaryDirectory() as repodir:
        with open(pjoin(repodir, "Dockerfile"), "w") as d:
            d.write("FROM andrewosh/some-image")

        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack(base_image)
            assert not bp.detect()


def test_legacy_on_repo_without_dockerfile(base_image):
    # check legacy buildpack doesn't trigger on a repo w/o Dockerfile
    with TemporaryDirectory() as repodir:
        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack(base_image)
            assert not bp.detect()


@pytest.mark.parametrize("python_version", ["2.6", "3.0", "4.10", "3.99"])
def test_unsupported_python(tmpdir, python_version, base_image):
    tmpdir.chdir()
    bp = PythonBuildPack(base_image)
    bp._python_version = python_version
    assert bp.python_version == python_version
    with pytest.raises(ValueError):
        bp.render()
