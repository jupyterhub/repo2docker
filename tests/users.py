"""
Test that User name and ID mapping works
"""
import os
import subprocess
import tempfile
import time

def test_user():
    """
    Validate user id and name setting
    """
    ts = str(time.time())
    with tempfile.TemporaryDirectory() as tmpdir:
        username = os.getlogin()
        subprocess.check_call([
            'repo2docker',
            '-v', '{}:/home/{}'.format(tmpdir, username),
            '--user-id', '1000',
            '--user-name', 'yuvipanda',
            tmpdir,
            '--',
            '/bin/bash',
            '-c', 'id -u > id && pwd > pwd && whoami > name && echo -n $USER > env_user'.format(ts)
        ])

        with open(os.path.join(tmpdir, 'id')) as f:
            assert f.read().strip() == '1000'
        with open(os.path.join(tmpdir, 'pwd')) as f:
            assert f.read().strip() == '/home/yuvipanda'
        with open(os.path.join(tmpdir, 'name')) as f:
            assert f.read().strip() == 'yuvipanda'
        with open(os.path.join(tmpdir, 'env_user')) as f:
            assert f.read().strip() == 'yuvipanda'
