import subprocess

def execute_cmd(cmd, capture=False, **kwargs):
    """
    Call given command, yielding output line by line if capture=True
    """
    if capture:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT

    proc = subprocess.Popen(cmd, **kwargs)

    if not capture:
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)
        return

    try:
        for line in iter(proc.stdout.readline, b''):
            yield line.decode('utf8', 'replace')
    finally:
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)
