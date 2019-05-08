"""
Test that build time memory limits are actually enforced.

We give the container image at least 128M of RAM (so base things like
apt and pip can run), and then try to allocate & use 256MB in postBuild.
This should fail!
"""

import os
import shutil
import time

from unittest.mock import MagicMock

import docker

import pytest

from repo2docker.app import Repo2Docker
from repo2docker.buildpacks import BaseImage, DockerBuildPack


basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def does_build(tmpdir, build_src_dir, mem_limit, mem_allocate_mb):
    builddir = tmpdir.join('build')
    shutil.copytree(build_src_dir, builddir)
    builddir.chdir()
    print(os.getcwd(), os.listdir('.'))
    mem_allocate_mb_file = os.path.join(builddir, 'mem_allocate_mb')

    # Cache bust so we actually do a rebuild each time this is run!
    with builddir.join('cachebust').open('w') as cachebust:
        cachebust.write(str(time.time()))

    # we don't have an easy way to pass env vars or whatever to
    # postBuild from here, so we write a file into the repo that is
    # read by the postBuild script!
    with open(mem_allocate_mb_file, 'w') as f:
        f.write(str(mem_allocate_mb))
    r2d = Repo2Docker(build_memory_limit=str(mem_limit) + 'M')
    r2d.initialize()
    try:
        r2d.build()
    except Exception:
        return False
    else:
        return True


@pytest.mark.parametrize(
    'test, mem_limit, mem_allocate_mb, expected',
    [
        ('dockerfile', 128, 256, False),
        ('dockerfile', 512, 256, True),
        ('non-dockerfile', 128, 256, False),
        ('non-dockerfile', 512, 256, True),
    ]
)
def test_memlimit_nondockerfile(tmpdir, test, mem_limit, mem_allocate_mb, expected):
    """
    Test if memory limited builds are working for non dockerfile builds
    """
    success = does_build(
        tmpdir,
        os.path.join(basedir, 'memlimit', test),
        mem_limit,
        mem_allocate_mb,
    )
    assert success == expected


def test_memlimit_same_postbuild():
    """
    Validate that the postBuild files for dockerfile & nondockerfile are same

    Until https://github.com/jupyter/repo2docker/issues/160 gets fixed.
    """
    filepaths = [
        os.path.join(basedir, 'memlimit', t, "postBuild")
        for t in ("dockerfile", "non-dockerfile")
    ]
    file_contents = []
    for fp in filepaths:
        with open(fp) as f:
            file_contents.append(f.read())
    # Make sure they're all the same
    assert len(set(file_contents)) == 1


@pytest.mark.parametrize('BuildPack', [BaseImage, DockerBuildPack])
def test_memlimit_argument_type(BuildPack):
    # check that an exception is raised when the memory limit isn't an int
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with pytest.raises(ValueError) as exc_info:
        for line in BuildPack().build(fake_client, 'image-2', "10Gi", {}, [], {}):
            pass

        assert "The memory limit has to be specified as an" in str(exc_info.value)
