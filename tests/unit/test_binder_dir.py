import os

import pytest

from repo2docker import buildpacks


@pytest.mark.parametrize("binder_dir", ["binder", ".binder", ""])
def test_binder_dir(tmpdir, binder_dir, base_image):
    tmpdir.chdir()
    if binder_dir:
        os.mkdir(binder_dir)

    bp = buildpacks.BuildPack(base_image)
    assert binder_dir == bp.binder_dir
    assert bp.binder_path("foo.yaml") == os.path.join(binder_dir, "foo.yaml")


def test_exclusive_binder_dir(tmpdir, base_image):
    tmpdir.chdir()
    os.mkdir("./binder")
    os.mkdir("./.binder")

    bp = buildpacks.BuildPack(base_image)
    with pytest.raises(RuntimeError):
        _ = bp.binder_dir
