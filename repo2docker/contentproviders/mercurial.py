import subprocess

from .base import ContentProvider, ContentProviderException
from ..utils import execute_cmd


hg_config = [
    "--config",
    "extensions.hggit=!",
    "--config",
    "extensions.evolve=",
    "--config",
    "extensions.topic=",
]


class Mercurial(ContentProvider):
    """Provide contents of a remote Mercurial repository."""

    def detect(self, source, ref=None, extra_args=None):
        if "github.com/" in source or source.endswith(".git"):
            return None
        try:
            subprocess.check_output(
                ["hg", "identify", source] + hg_config, stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            return None

        return {"repo": source, "ref": ref}

    def fetch(self, spec, output_dir, yield_output=False):
        repo = spec["repo"]
        ref = spec.get("ref", None)

        # make a clone of the remote repository
        try:
            cmd = ["hg", "clone", repo, output_dir]
            cmd.extend(hg_config)
            if ref is not None:
                # don't update so the clone will include an empty working
                # directory, the given ref will be updated out later
                cmd.extend(["--noupdate"])
            for line in execute_cmd(cmd, capture=yield_output):
                yield line

        except subprocess.CalledProcessError as error:
            msg = "Failed to clone repository from {repo}".format(repo=repo)
            if ref is not None:
                msg += " (ref {ref})".format(ref=ref)
            msg += "."
            raise ContentProviderException(msg) from error

        # check out the specific ref given by the user
        if ref is not None:
            try:
                for line in execute_cmd(
                    ["hg", "update", "--clean", ref] + hg_config,
                    cwd=output_dir,
                    capture=yield_output,
                ):
                    yield line
            except subprocess.CalledProcessError:
                self.log.error(
                    "Failed to update to ref %s", ref, extra=dict(phase="failed")
                )
                raise ValueError("Failed to update to ref {}".format(ref))

        cmd = ["hg", "identify"]
        cmd.extend(hg_config)
        sha1 = subprocess.Popen(cmd, stdout=subprocess.PIPE, cwd=output_dir)
        self._sha1 = sha1.stdout.read().decode().strip()

    @property
    def content_id(self):
        """A unique ID to represent the version of the content.
        Uses the first seven characters of the git commit ID of the repository.
        """
        return self._sha1[:7]
