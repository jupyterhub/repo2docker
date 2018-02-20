"""
Test that environment variables may be defined
"""
import os
import subprocess
import tempfile
import time

def test_env():
    """
    Validate that you can define environment variables
    """
    ts = str(time.time())
    with tempfile.TemporaryDirectory() as tmpdir:
        username = os.getlogin()
        subprocess.check_call([
            'repo2docker',
            '-v', '{}:/home/{}'.format(tmpdir, username),
            '-e', 'FOO={}'.format(ts), 
            '--env', 'BAR=baz',
            '--',
            tmpdir,
            '/bin/bash',
            '-c', 'echo -n $FOO > ts && echo -n $BAR > bar'
        ])

        with open(os.path.join(tmpdir, 'ts')) as f:
            assert f.read().strip() == ts
        with open(os.path.join(tmpdir, 'bar')) as f:
            assert f.read().strip() == 'baz'

