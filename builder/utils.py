import subprocess

def execute_cmd(cmd):
    """
    Call given command, yielding output line by line
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    try:
        for line in iter(proc.stdout.readline, ''):
            yield line.rstrip()
    finally:
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)
