"""
Base classes for repo2docker ContentProviders

ContentProviders accept a `spec` of various kinds, and
provide the contents from the spec to a given output directory.
"""
import logging
import os


class ContentProviderException(Exception):
    """Exception raised when a ContentProvider can not provide content."""
    pass


class ContentProvider:
    def __init__(self):
        self.log = logging.getLogger("repo2docker")

    def detect(self, repo, ref=None, extra_args=None):
        """Determine compatibility between source and this provider.

        If the provider knows how to fetch this source it will return a
        `spec` that can be passed to `fetch`. The arguments are the `repo`
        string passed on the command-line, the value of the --ref parameter,
        if provided and any provider specific arguments provided on the
        command-line.

        If the provider does not know how to fetch this source it will return
        `None`.
        """
        raise NotImplementedError()

    def fetch(self, spec, output_dir, yield_output=False):
        """Provide the contents of given spec to output_dir

        This generator yields logging information if `yield_output=True`,
        otherwise log output is printed to stdout.

        Arguments:
            spec -- Dict specification understood by this ContentProvider
            output_dir {string} -- Path to output directory (must already exist)
            yield_output {bool} -- If True, return output line by line. If not,
                                   output just goes to stdout.
        """
        raise NotImplementedError()


class Local(ContentProvider):
    def detect(self, source, ref=None, extra_args=None):
        if os.path.isdir(source):
            return {'path': source}

    def fetch(self, spec, output_dir, yield_output=False):
        # nothing to be done if your content is already in the output directory
        msg = "Local content provider assumes {} == {}".format(spec['path'],
                                                               output_dir)
        assert output_dir == spec['path'], msg
        yield
