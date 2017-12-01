"""
Test that build time memory limits are actually enforced.

We give the container image at least 128M of RAM (so base things like
apt and pip can run), and then try to allocate & use 256MB in postBuild.
This should fail!
"""
import os
import subprocess
import time

def does_build(builddir, mem_limit, mem_allocate_mb):
    mem_allocate_mb_file = os.path.join(builddir, 'mem_allocate_mb')

    # Cache bust so we actually do a rebuild each time this is run!
    with open(os.path.join(builddir, 'cachebust'), 'w') as cachebust:
        cachebust.write(str(time.time()))
    try:
        with open(mem_allocate_mb_file, 'w') as f:
            f.write(str(mem_allocate_mb))
        try:
            output = subprocess.check_output(
                [
                    'repo2docker',
                    '--no-run',
                    '--build-memory-limit', '{}M'.format(mem_limit),
                    builddir
                ],
                stderr=subprocess.STDOUT,
            ).decode()
            print(output)
            return True
        except subprocess.CalledProcessError as e:
            output = e.output.decode()
            print(output)
            if "The command '/bin/sh -c ./postBuild' returned a non-zero code: 137" in output:
                return False
            else:
                raise
    finally:
        os.remove(mem_allocate_mb_file)



def test_memlimit_nondockerfile_fail():
    """
    Test if memory limited builds are working for non dockerfile builds
    """
    basedir = os.path.dirname(__file__)
    assert not does_build(
        os.path.join(basedir, 'memlimit/non-dockerfile'),
        128,
        256
    )
    assert does_build(
        os.path.join(basedir, 'memlimit/non-dockerfile'),
        512,
        256
    )


def test_memlimit_dockerfile_fail():
    """
    Test if memory limited builds are working for dockerfile builds
    """
    basedir = os.path.dirname(__file__)
    assert not does_build(
        os.path.join(basedir, 'memlimit/dockerfile'),
        128,
        256
    )

    assert does_build(
        os.path.join(basedir, 'memlimit/dockerfile'),
        512,
        256
    )
