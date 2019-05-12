import os

import pytest

from repo2docker import buildpacks


@pytest.mark.parametrize("binder_dir", ['.binder', 'binder'])
def test_binder_dir_property(tmpdir, binder_dir):
    tmpdir.chdir()
    os.mkdir(binder_dir)

    bp = buildpacks.BuildPack()
    assert binder_dir in bp.binder_dir
    assert bp.binder_path('foo.yaml') == os.path.join(binder_dir, 'foo.yaml')


def test_root_binder_dir(tmpdir):
    tmpdir.chdir()
    bp = buildpacks.BuildPack()
    assert bp.binder_dir == ''


def test_exclusive_binder_dir(tmpdir):
    tmpdir.chdir()
    os.mkdir('./binder')
    os.mkdir('./.binder')

    bp = buildpacks.BuildPack()
    with pytest.raises(RuntimeError):
        _ = bp.binder_dir
