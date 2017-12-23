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


class ImageNameValidator:
    """
    Given a docker image_name, check if the image_name conforms to the restrictions placed by docker.

    Class defines the regex patterns based off of the definitions in
    https://github.com/docker/distribution/blob/master/reference/regexp.go. There are some modifications as noted below.
    """

    def __init__(self):
        alpha_numeric_regex = r'[a-z0-9]+'
        """str: raw pattern denoting only lowercase character and numbers part of name"""

        separator_regex = r'(?:[\._]|__|[-]*)'
        """str: raw pattern denoting separators allowed to be embedded in component names"""

        domain_component_regex_lowercase = r'(?:[a-z0-9]|[a-z0-9][a-z0-9-]*[a-z0-9])'
        """str: raw pattern restricts the domain component of the tag to have at least 3 lowercase alphabets or numbers
        Different from the https://github.com/docker/distribution/blob/master/reference/regexp.go in the sense only allow
        lowercase characters
        """

        domain_component_regex = r'(?:[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])'
        """str: raw pattern restricts the domain component of the tag to have at least 3 alphabets or numbers"""

        numbers = r'[0-9]+'
        """str: raw pattern restricts to only one or more numbers"""

        tag_regex = r'[\w][\w.-]{0,127}'
        """str: raw pattern matching valid tag names that can at most contain 128 characters"""

        digest_regex = r'[A-Za-z][A-Za-z0-9]*(?:[-_+.][A-Za-z][A-Za-z0-9]*)*[:][[:xdigit:]]{32,}'
        """str: raw patten representing an image digest"""

        name_component_regex = self.expression(alpha_numeric_regex,
                                               self.optional(self.repeated(separator_regex,
                                                                           alpha_numeric_regex)
                                                             )
                                               )
        """str: restricts registry path component to start with alpha_numeric_regex followed by optional parts that can
        have separators"""

        domain_regex = self.expression(domain_component_regex_lowercase,
                                       self.optional(self.repeated(r'\.', domain_component_regex)),
                                       self.optional(r':', numbers))
        """str: representing a registry domain starting with domain_component_regex followed by option period separated
        domain_component_regex followed by optional : separated port

        Example:

        'test.Com/name:latest' is still a valid tag
        but
        'Test/name:latest' is not a valid tag

        Note:

        This give a stricter pattern as in the first part in a '.' separated registry domain must always be lowercase

        This pattern will not allow cases like
        'TEST.com/name:latest' though docker considers it a valid tag
        """

        name_regex = self.expression(self.optional(domain_regex, r'/'),
                                     name_component_regex,
                                     self.optional(self.repeated(r'/', name_component_regex)))
        """str: defines a pattern representing an optional  registry domain followed by one or more component names
        separated by /"""

        self.reference_regex = self.anchored(self.capture(name_regex),
                                             self.optional(r':', self.capture(tag_regex)),
                                             self.optional(r'@', digest_regex))
        """str: defines a pattern representing a reference. The pattern is anchored and has capturing groups for
        name, tag and digest"""

    @staticmethod
    def is_valid_image_name(image_name):
        """
        Static method that tests whether image_name conforms to a reference pattern

        Args:
            image_name: string representing the image name

        Returns:
             True if it a valid docker image name
        """

        validator = ImageNameValidator()
        result = re.match(validator.reference_regex, image_name)

        return result is not None

    def expression(self, *args):
        """
        Defines a full expression where each regex must follow the other
        Args:
            *args: Argument list representing regex

        Returns:
            an expression which is a concatenation of the regexes in the *args
        """
        s = r''.join(list(args))
        return s

    def optional(self, *args):
        """
        Wraps the expression in a non-capturing group and makes it optional

        Args:
            *args: Argument list representing regex

        Returns:
            a string representing the regex wrapped in non-capturing group with optional production
        """
        return self.group(self.expression(*args)) + r'?'

    def repeated(self, *args):
        """
        Wraps the expression in a non-capturing group to get one or more matches

        Args:
            *args: Argument list representing regex

        Returns:
            a string representing the regex wrapped in non-capturing group with one or more matches
        """
        return self.group(self.expression(*args)) + r'+'

    def group(self, *args):
        """
        Wraps the expression in a non-capturing group

        Args:
            *args: Argument list representing regex

        Returns:
            wraps the expression represented by args in non-capturing group
        """
        return r'(?:' + self.expression(*args) + r')'

    def capture(self, *args):
        """
        Wraps the expression in a capturing group

        Args:
            *args: Argument list representing regex

        Returns:
            wraps the expression represented by args in capturing group
        """
        return r'(' + self.expression(*args) + r')'

    def anchored(self, *args):
        """
        Anchors the regular expression by adding start and end delimiters

        Args:
            *args: Argument list representing regex

        Returns:
            anchored regex
        """
        return r'^' + self.expression(*args) + r'$'