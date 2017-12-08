from contextlib import contextmanager
from functools import partial
import shutil
import subprocess

from traitlets import Integer

def execute_cmd(cmd, capture=False, **kwargs):
    """
    Call given command, yielding output line by line if capture=True
    """
    if capture:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT

    proc = subprocess.Popen(cmd, **kwargs)

    if not capture:
        # not capturing output, let the subprocesses talk directly
        # to the terminal
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


@contextmanager
def maybe_cleanup(path, cleanup=False):
    yield
    if cleanup:
        shutil.rmtree(path, ignore_errors=True)


class ByteSpecification(Integer):
    """
    Allow easily specifying bytes in units of 1024 with suffixes

    Suffixes allowed are:
      - K -> Kilobyte
      - M -> Megabyte
      - G -> Gigabyte
      - T -> Terabyte

    Stolen from JupyterHub
    """

    UNIT_SUFFIXES = {
        'K': 1024,
        'M': 1024 * 1024,
        'G': 1024 * 1024 * 1024,
        'T': 1024 * 1024 * 1024 * 1024,
    }

    # Default to allowing None as a value
    allow_none = True

    def validate(self, obj, value):
        """
        Validate that the passed in value is a valid memory specification

        It could either be a pure int, when it is taken as a byte value.
        If it has one of the suffixes, it is converted into the appropriate
        pure byte value.
        """
        if isinstance(value, (int, float)):
            return int(value)

        try:
            num = float(value[:-1])
        except ValueError:
            raise TraitError('{val} is not a valid memory specification. Must be an int or a string with suffix K, M, G, T'.format(val=value))
        suffix = value[-1]
        if suffix not in self.UNIT_SUFFIXES:
            raise TraitError('{val} is not a valid memory specification. Must be an int or a string with suffix K, M, G, T'.format(val=value))
        else:
            return int(float(num) * self.UNIT_SUFFIXES[suffix])
