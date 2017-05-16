import subprocess

def execute_cmd(cmd):
    """
    Call given command, yielding output line by line
    """
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) as proc:
        for line in iter(proc.stdout.readline, ''):
            yield line.rstrip()
