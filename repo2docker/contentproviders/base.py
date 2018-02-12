"""
Base classes for repo2docker ContentProviders

ContentProviders accept a `spec` of various kinds, and 
provide the contents from the spec to a given output directory.
"""
class ContentProviderException(Exception):
    """Exception raised when a ContentProvider can not provide content
    """
    pass

class ContentProvider:
    kind = ""

    def provide(self, spec, output_dir, yield_output=False):
        """Provide the contents of given spec to output_dir

        This is a generator, and so should be yielded from or iterated over.
        
        Arguments:
            spec -- Dict / String specification understood by this ContentProvider
            output_dir {string} -- Path to output directory (must already exist)
            yield_output {bool} -- If True, return output line by line. If not, output just goes to stdout.
        """
        raise NotImplementedError()

