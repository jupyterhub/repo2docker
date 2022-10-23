import subprocess

from .base import ContentProvider, ContentProviderException
from ..utils import execute_cmd, check_ref, R2dState


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
            for line in execute_cmd(cmd, capture=yield_output):
                yield line

        except subprocess.CalledProcessError as e:
            msg = "Failed to clone repository from {repo}".format(repo=repo)
            if ref != "HEAD":
                msg += " (ref {ref})".format(ref=ref)
            msg += "."
            raise ContentProviderException(msg) from e

        # check out the specific ref given by the user
        if ref != "HEAD":
            hash = check_ref(ref, output_dir)
            if hash is None:
                self.log.error(
                    "Failed to check out ref %s", ref, extra=dict(phase=R2dState.FAILED)
                )
                if ref == "master":
                    msg = (
                        "Failed to check out the 'master' branch. "
                        "Maybe the default branch is not named 'master' "
                        "for this repository.\n\nTry not explicitly "
                        "specifying `--ref`."
                    )
                else:
                    msg = "Failed to check out ref {}".format(ref)
                raise ValueError(msg)
            # We don't need to explicitly checkout things as the reset will
            # take care of that. If the hash is resolved above, we should be
            # able to reset to it
            for line in execute_cmd(
                ["git", "reset", "--hard", hash], cwd=output_dir, capture=yield_output
            ):
                yield line

        # ensure that git submodules are initialised and updated
        #
        # WARNING: To pass `-c protocol.file.allow=always` is a workaround to a
        #          security patch and can have real implications, we must
        #          evaluate if we can do this or if we can handle this another
        #          way instead.
        #
        #          https://github.com/jupyterhub/repo2docker/issues/1198#issuecomment-1288114992
        #          https://bugs.launchpad.net/ubuntu/+source/git/+bug/1993586
        #
        for line in execute_cmd(
            [
                "git",
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "update",
                "--init",
                "--recursive",
            ],
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
