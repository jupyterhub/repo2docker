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
    username = 'yuvipanda'
    with tempfile.TemporaryDirectory() as tmpdir:
        subprocess.check_call([
            'repo2docker',
            '-v', '{}:/home/{}'.format(tmpdir, username),
            '--user-id', '1000',
            '--user-name', username,
            tmpdir,
            '--',
            '/bin/bash',
            '-c', 'id -u > id && pwd > pwd && whoami > name && echo -n $USER > env_user'.format(ts)
        ])

        with open(os.path.join(tmpdir, 'id')) as f:
            assert f.read().strip() == '1000'
        with open(os.path.join(tmpdir, 'pwd')) as f:
            assert f.read().strip() == '/home/{}'.format(username)
        with open(os.path.join(tmpdir, 'name')) as f:
            assert f.read().strip() == username
        with open(os.path.join(tmpdir, 'name')) as f:
            assert f.read().strip() == username
