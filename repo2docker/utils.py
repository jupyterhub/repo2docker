from contextlib import contextmanager
from functools import partial
import os
import re
import subprocess

from traitlets import Integer, TraitError


def execute_cmd(cmd, capture=False, **kwargs):
    """
    Call given command, yielding output line by line if capture=True.

    Must be yielded from.
    """
    if capture:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.STDOUT

    proc = subprocess.Popen(cmd, **kwargs)

    if not capture:
        # not capturing output, let subprocesses talk directly to terminal
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
        """Flush next line of the buffer"""
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
def chdir(path):
    """Change working directory to `path` and restore it again

    This context maanger is useful if `path` stops existing during your
    operations.
    """
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_dir)


def validate_and_generate_port_mapping(port_mappings):
    """
    Validate a list of port mappings and return a dictionary of port mappings.

    Args:
        port_mappings (list): List of strings of format
            `'host_port:container_port'` with optional tcp udp values and host
            network interface

    Returns:
        Dictionary of port mappings in the format accepted by docker-py's
        `containers.run()` method (https://docker-py.readthedocs.io/en/stable/containers.html)

    Raises:
        Exception on invalid port mapping

    Note:
        One limitation of repo2docker is it cannot bind a
        single container_port to multiple host_ports
        (docker-py supports this but repo2docker does not)
    """
    def check_port(port):
        try:
            p = int(port)
        except ValueError as e:
            raise ValueError('Port specification "{}" has '
                             'an invalid port.'.format(mapping))
        if p > 65535:
            raise ValueError('Port specification "{}" specifies '
                             'a port above 65535.'.format(mapping))
        return port

    def check_port_string(p):
        parts = p.split('/')
        if len(parts) == 2:  # 134/tcp
            port, protocol = parts
            if protocol not in ('tcp', 'udp'):
                raise ValueError('Port specification "{}" has '
                                 'an invalid protocol.'.format(mapping))
        elif len(parts) == 1:
            port = parts[0]
            protocol = 'tcp'

        check_port(port)

        return '/'.join((port, protocol))

    ports = {}
    if port_mappings is None:
        return ports

    for mapping in port_mappings:
        parts = mapping.split(':')

        *host, container_port = parts
        # just a port
        if len(host) == 1:
            host = check_port(host[0])
        else:
            host = tuple((host[0], check_port(host[1])))

        container_port = check_port_string(container_port)
        ports[container_port] = host

    return ports


def is_valid_docker_image_name(image_name):
    """
    Determine if image name is valid for docker using strict pattern.

    Function that constructs a regex representing the docker image name and
    tests it against the given image_name. Reference Regex definition in
    https://github.com/docker/distribution/blob/master/reference/regexp.go
    The definition uses a stricter pattern than the docker default.

    Args:
        image_name: string representing a docker image name

    Returns:
        True if image_name is valid, else False

    Example:
        'test.Com/name:latest' is a valid tag

        'Test/name:latest' is not a valid tag

    Note:
        This function has a stricter pattern than
        https://github.com/docker/distribution/blob/master/reference/regexp.go

        This pattern will not allow cases like `TEST.com/name:latest` though
        docker considers it a valid tag.
    """
    reference_regex = re.compile(r"""
        ^  # Anchored at start and end of string

        (  # Start capturing name

        (?:  # start grouping the optional registry domain name part

        (?:[a-z0-9]|[a-z0-9][a-z0-9-]*[a-z0-9])  # lowercase only '<domain-name-component>'

        (?:  # start optional group

        # multiple repetitions of pattern '.<domain-name-component>'
        (?:\.(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]))+

        )?  # end optional grouping part of the '.' separated domain name

        (?::[0-9]+)?/  # '<domain-name>' followed by an optional '<port>' component followed by '/' literal

        )?  # end grouping the optional registry domain part

        # start <name-pattern>
        [a-z0-9]+   # must have a <name-component>
        (?:
        (?:(?:[\._]|__|[-]*)[a-z0-9]+)+  # repeat the pattern '<separator><name-component>'
        )?  # optionally have multiple repetitions of the above line
        # end <name-pattern>

        (?:  # start optional name components

        (?:  # start multiple repetitions

        /   # separate multiple name components by /
        # start <name-pattern>
        [a-z0-9]+                        # must have a <name-component>
        (?:
        (?:(?:[\._]|__|[-]*)[a-z0-9]+)+  # repeat the pattern '<separator><name-component>'
        )?                               # optionally have multiple repetitions of the above line
        # end <name-pattern>

        )+  # multiple repetitions of the pattern '/<name-component><separator><name-component>'

        )?  # optionally have the above group

        )   # end capturing name

        (?::([\w][\w.-]{0,127}))?    # optional capture <tag-pattern>=':<tag>'
        # optionally capture <digest-pattern>='@<digest>'
        (?:@[A-Za-z][A-Za-z0-9]*(?:[-_+.][A-Za-z][A-Za-z0-9]*)*[:][A-Fa-f0-9]{32,})?
        $
        """, re.VERBOSE)

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
        Validate that the passed-in value is a valid memory specification

        If value is a pure int, it is taken as a byte value.
        If value has one of the unit suffixes, it is converted into the
        appropriate pure byte value.
        """
        if isinstance(value, (int, float)):
            return int(value)

        try:
            num = float(value[:-1])
        except ValueError:
            raise TraitError(
                '{val} is not a valid memory specification. '
                'Must be an int or a string with suffix K, M, G, T'
                .format(val=value)
            )
        suffix = value[-1]
        if suffix not in self.UNIT_SUFFIXES:
            raise TraitError(
                '{val} is not a valid memory specification. '
                'Must be an int or a string with suffix K, M, G, T'
                .format(val=value)
            )
        else:
            return int(float(num) * self.UNIT_SUFFIXES[suffix])


def check_ref(ref, cwd=None):
    """Prepare a ref and ensure it works with git reset --hard."""
    # Try original ref, then trying a remote ref, then removing remote
    refs = [ref,                        # Original ref
            '/'.join(["origin", ref]),  # In case its a remote branch
            ref.split('/')[-1]]         # In case partial commit w/ remote

    hash = None
    for i_ref in refs:
        call = ["git", "rev-parse", "--quiet", i_ref]
        try:
            # If success, output will be <hash>
            response = subprocess.check_output(call, stderr=subprocess.DEVNULL, cwd=cwd)
            hash = response.decode().strip()
        except Exception:
            # We'll throw an error later if no refs resolve
            pass
    return hash
