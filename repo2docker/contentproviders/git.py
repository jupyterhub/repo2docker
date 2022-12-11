import subprocess

from ..utils import R2dState, check_ref, execute_cmd
from .base import ContentProvider, ContentProviderException


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
        ref = spec.get("ref") or "HEAD"

        # make a, possibly shallow, clone of the remote repository
        try:
            cmd = ["git", "clone"]
            if ref == "HEAD":
                # check out of HEAD is performed after the clone is complete
                cmd.extend(["--depth", "1"])
            else:
                # don't check out HEAD, the given ref will be checked out later
                # this prevents HEAD's submodules to be cloned if ref doesn't have them
                cmd.extend(["--no-checkout"])
            cmd.extend([repo, output_dir])
            yield from execute_cmd(cmd, capture=yield_output)

        except subprocess.CalledProcessError as e:
            msg = f"Failed to clone repository from {repo}"
            if ref != "HEAD":
                msg += f" (ref {ref})"
            msg += "."
            raise ContentProviderException(msg) from e

        # check out the specific ref given by the user
        if ref != "HEAD":
            hash = check_ref(ref, output_dir)
            if hash is None:
                self.log.error(
                    f"Failed to check out ref {ref}", extra=dict(phase=R2dState.FAILED)
                )
                if ref == "master" or ref == "main":
                    msg = (
                        f"Failed to check out the '{ref}' branch. "
                        f"Maybe the default branch is not named '{ref}' "
                        "for this repository.\n\nTry not explicitly "
                        "specifying `--ref`."
                    )
                else:
                    msg = f"Failed to check out ref {ref}"
                raise ValueError(msg)
            # We don't need to explicitly checkout things as the reset will
            # take care of that. If the hash is resolved above, we should be
            # able to reset to it
            yield from execute_cmd(
                ["git", "reset", "--hard", hash], cwd=output_dir, capture=yield_output
            )

        # ensure that git submodules are initialised and updated
        yield from execute_cmd(
            ["git", "submodule", "update", "--init", "--recursive"],
            cwd=output_dir,
            capture=yield_output,
        )

        cmd = ["git", "rev-parse", "HEAD"]
        sha1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=output_dir)
        self._sha1 = sha1.stdout.read().decode().strip()

    @property
    def content_id(self):
        """A unique ID to represent the version of the content.
        Uses the first seven characters of the git commit ID of the repository.
        """
        return self._sha1[:7]
