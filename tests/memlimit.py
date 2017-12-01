import subprocess

def test_memlimit_nondockerfile():
    """
    Test if memory limited builds are working for non dockerfile builds
    """
    try:
        subprocess.check_call([
            'repo2docker',
            '--no-run',
            '--build-memory-limit', '4M',
            'tests/memlimit/non-dockerfile'
        ])
        # If this doesn't throw an exception, then memory limit was
        # not enforced!
        assert False
    except subprocess.CalledProcessError as e:
        assert True


def test_memlimit_dockerfile():
    """
    Test if memory limited builds are working for non dockerfile builds
    """
    try:
        subprocess.check_call([
            'repo2docker',
            '--no-run',
            '--build-memory-limit', '4M',
            'tests/memlimit/dockerfile'
        ])
        # If this doesn't throw an exception, then memory limit was
        # not enforced!
        assert False
    except subprocess.CalledProcessError as e:
        assert True
