import subprocess
import sys

from .base import ContentProvider, ContentProviderException
from ..utils import execute_cmd, check_ref


class Git(ContentProvider):
    """Provide contents of a remote git repository."""

    def detect(self, source, ref=None, extra_args=None):
        # Git is our content provider of last resort. This is to maintain the
        # old behaviour when git and local directories were the only supported
        # content providers. This means that this content provider will always
        # match. The downside is that the call to `fetch()` later on might fail
        return {"repo": source, "ref": ref}

    def fetch(self, spec, output_dir, yield_output=False):
        repo = spec["repo"]
        ref = spec.get("ref", None)

        # make a, possibly shallow, clone of the remote repository
        try:
            cmd = ["git", "clone"]
            if ref is None:
                # check out of HEAD is performed after the clone is complete
                cmd.extend(["--depth", "1"])
            else:
                # don't check out HEAD, the given ref will be checked out later
                # this prevents HEAD's submodules to be cloned if ref doesn't have them
                cmd.extend(["--no-checkout"])
            cmd.extend([repo, output_dir])
            for line in execute_cmd(cmd, capture=yield_output):
                yield line

        except subprocess.CalledProcessError as e:
            msg = "Failed to clone repository from {repo}".format(repo=repo)
            if ref is not None:
                msg += " (ref {ref})".format(ref=ref)
            msg += "."
            raise ContentProviderException(msg) from e

        # check out the specific ref given by the user
        if ref is not None:
            hash = check_ref(ref, output_dir)
            if hash is None:
                self.log.error(
                    "Failed to check out ref %s", ref, extra=dict(phase="failed")
                )
                raise ValueError("Failed to check out ref {}".format(ref))
            # We don't need to explicitly checkout things as the reset will
            # take of that. If the hash is resolved above, we should be
            # able to reset to it
            for line in execute_cmd(
                ["git", "reset", "--hard", hash], cwd=output_dir, capture=yield_output
            ):
                yield line

        # ensure that git submodules are initialised and updated
        for line in execute_cmd(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=output_dir,
            capture=yield_output,
        ):
            yield line

        cmd = ["git", "rev-parse", "HEAD"]
        sha1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=output_dir)
        self._sha1 = sha1.stdout.read().decode().strip()

    @property
    def content_id(self):
        """A unique ID to represent the version of the content.
        Uses the first seven characters of the git commit ID of the repository.
        """
        return self._sha1[:7]
