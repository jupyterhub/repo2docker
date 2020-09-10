import subprocess
import os
from distutils.util import strtobool

from .base import ContentProvider, ContentProviderException
from ..utils import execute_cmd

HG_EVOLVE_REQUIRED = strtobool(
    os.environ.get("REPO2DOCKER_HG_EVOLVE_REQUIRED", "False")
)

if HG_EVOLVE_REQUIRED:
    if "REPO2DOCKER_HG_REQUIRED" in os.environ:
        HG_REQUIRED = strtobool(os.environ["REPO2DOCKER_HG_REQUIRED"])
        if not HG_REQUIRED:
            raise ValueError(
                "Incompatible values for environment variables "
                "REPO2DOCKER_HG_EVOLVE_REQUIRED=1 and REPO2DOCKER_HG_REQUIRED=0"
            )
    else:
        HG_REQUIRED = True
else:
    HG_REQUIRED = strtobool(os.environ.get("REPO2DOCKER_HG_REQUIRED", "False"))


def is_mercurial_available():
    try:
        subprocess.check_output(["hg", "version"])
    except subprocess.CalledProcessError:
        return False
    return True


if HG_REQUIRED and not is_mercurial_available():
    raise RuntimeError("REPO2DOCKER_HG_REQUIRED but the command `hg` is not available")


class Mercurial(ContentProvider):
    """Provide contents of a remote Mercurial repository."""

    def detect(self, source, ref=None, extra_args=None):
        if "github.com/" in source or source.endswith(".git"):
            return None
        try:
            subprocess.check_output(
                ["hg", "identify", source, "--config", "extensions.hggit=!"],
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            # warning: if hg is not installed and `not HG_REQUIRED`,
            # we return None even for a hg repo
            return None

        return {"repo": source, "ref": ref}

    def fetch(self, spec, output_dir, yield_output=False):
        repo = spec["repo"]
        ref = spec.get("ref", None)

        # make a clone of the remote repository
        try:
            cmd = [
                "hg",
                "clone",
                repo,
                output_dir,
                "--config",
                "phases.publish=False",
            ]
            if ref is not None:
                # don't update so the clone will include an empty working
                # directory, the given ref will be updated out later
                cmd.extend(["--noupdate"])
            for line in execute_cmd(cmd, capture=yield_output):
                yield line

        except subprocess.CalledProcessError as error:
            msg = f"Failed to clone repository from {repo}"
            if ref is not None:
                msg += f" (ref {ref})"
            msg += "."
            raise ContentProviderException(msg) from error

        # check out the specific ref given by the user
        if ref is not None:
            try:
                for line in execute_cmd(
                    ["hg", "update", "--clean", ref],
                    cwd=output_dir,
                    capture=yield_output,
                ):
                    yield line
            except subprocess.CalledProcessError:
                self.log.error(
                    "Failed to update to ref %s", ref, extra=dict(phase="failed")
                )
                raise ValueError("Failed to update to ref {}".format(ref))

        cmd = ["hg", "identify", "-i"]
        sha1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=output_dir)
        self._node_id = sha1.stdout.read().decode().strip()

    @property
    def content_id(self):
        """A unique ID to represent the version of the content."""
        return self._node_id
