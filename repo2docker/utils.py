from functools import partial
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
        # not capturing output, let the subprocesses talk directly to the terminal
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)
        return

    # Capture output for logging.
    # Each line will be yielded as text.
    # This should behave the same as .readline(), but splits on `\r` OR `\n`,
    # not just `\n`.
    buf = []
    def flush():
        line = b''.join(buf).decode('utf8', 'replace')
        buf[:] = []
        return line

    c_last = ''
    try:
        for c in iter(partial(proc.stdout.read, 1), b''):
            if c_last == b'\r' and buf and c != b'\n':
                yield flush()
            buf.append(c)
            if c == b'\n':
                yield flush()
            c_last = c
    finally:
        ret = proc.wait()
        if ret != 0:
            raise subprocess.CalledProcessError(ret, cmd)


def generate_repo_name(repo, ref):
    """Try to parse the repo string to extract relevant information.

    If we don't know what to do with a repo, just return the string.
    """
    if 'github.com' in repo:
        parts = repo.split('github.com/')[-1].split('/')
        org = parts[0]
        repo = parts[1]
        s = 'org-{org}_repo-{repo}'.format(org=org, repo=repo)
        if ref is not None:
            s += '_ref-{ref}'.format(ref=ref)
    else:
        s = repo
    s += '_'  # End with _ so we can separate it from the time
    return s
