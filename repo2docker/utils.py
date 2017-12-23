from contextlib import contextmanager
from functools import partial
import shutil
import subprocess
import re

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


def is_valid_docker_image_name(image_name):
    """
    Function that constructs a regex representing the docker image name and tests it against the given image_name
    Reference Regex definition in https://github.com/docker/distribution/blob/master/reference/regexp.go

    Args:
        image_name: string representing a docker image name

    Returns:
        True if image_name is valid else False

    Example:

        'test.Com/name:latest' is a valid tag

        'Test/name:latest' is not a valid tag

        Note:

        This function has a stricter pattern than https://github.com/docker/distribution/blob/master/reference/regexp.go

        This pattern will not allow cases like
        'TEST.com/name:latest' though docker considers it a valid tag
    """
    reference_regex = re.compile(r"""^ # Anchored at start and end of string

                        ( # Start capturing name

                        (?: # start grouping the optional registry domain name part

                        (?:[a-z0-9]|[a-z0-9][a-z0-9-]*[a-z0-9]) # lowercase only '<domain-name-component>'

                        (?: # start optional group

                        (?:\.(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]))+ # multiple repetitions of pattern '.<domain-name-component>'

                        )? # end optional grouping part of the '.' separated domain name

                        (?::[0-9]+)?/ # '<domain-name>' followed by an optional '<port>' component followed by '/' literal

                        )? # end grouping the optional registry domain part

                        # start <name-pattern>
                        [a-z0-9]+   # must have a <name-component>
                        (?:
                        (?:(?:[\._]|__|[-]*)[a-z0-9]+)+ # repeat the pattern '<separator><name-component>'
                        )? # optionally have multiple repetitions of the above line
                        # end <name-pattern>

                        (?: # start optional name components

                        (?: # start multiple repetitions

                        /   # separate multiple name components by /
                        # start <name-pattern>
                        [a-z0-9]+ # must have a <name-component>
                        (?:
                        (?:(?:[\._]|__|[-]*)[a-z0-9]+)+ # repeat the pattern '<separator><name-component>'
                        )? # optionally have multiple repetitions of the above line
                        # end <name-pattern>

                        )+ # multiple repetitions of the pattern '/<name-component><separator><name-component>'

                        )? # optionally have  the above group

                        ) # end capturing name

                        (?::([\w][\w.-]{0,127}))? # optional capture <tag-pattern>=':<tag>'
                        (?:@[A-Za-z][A-Za-z0-9]*(?:[-_+.][A-Za-z][A-Za-z0-9]*)*[:][[:xdigit:]]{32,})? # optionally capture <digest-pattern>='@<digest>'
                        $""",
                                 re.VERBOSE)

    return reference_regex.match(image_name) is not None


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
