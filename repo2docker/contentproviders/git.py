import subprocess

from .base import ContentProvider, ContentProviderException
from ..utils import execute_cmd

class GitContentProvider(ContentProvider):
    """Provides contents of a git repository (optionally at a given ref)
    """
    kind = "git"

    def provide(self, spec, output_dir, yield_output=False):
        url = spec['url']
        ref = spec.get('ref', None)
        try:
            for line in execute_cmd(['git', 'clone', url, output_dir],
                                    capture=yield_output):
                yield line
        except subprocess.CalledProcessError as e:
            raise ContentProviderException("Failed to clone repository!") from e

        if ref:
            try:
                for line in execute_cmd(['git', 'reset', '--hard', ref],
                                        cwd=output_dir,
                                        capture=yield_output):
                    yield line
            except subprocess.CalledProcessError:
                raise ContentProviderException("Failed to checkout ref {}!".format(ref)) from e
