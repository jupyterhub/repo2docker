"""
Test that volume mounts work when running
"""
import os
import subprocess
import tempfile
import time

def test_volume_home():
    """
    Validate that you can bind mount a volume onto homedirectory & write to it
    """
    ts = str(time.time())
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.check_call([
            'repo2docker',
            '-v', '{}:/home/jovyan'.format(tmpdir),
            tmpdir,
            '--',
            '/bin/bash',
            '-c', 'echo -n {} > ts'.format(ts)
        ])

        with open(os.path.join(tmpdir, 'ts')) as f:
            assert f.read() == ts
