"""BuildPack for extending existing container images."""

import os
import re
from functools import lru_cache

from ..base import BuildPack

# Matches an explicit `oci-image:<image>[:<tag>]` reference in runtime.txt.
# The image reference itself is registry-agnostic: Docker Hub, GCR, GAR,
# ECR, ACR, or a self-hosted registry are all just opaque strings after the
# prefix, so there's no need to special-case any particular registry's
# hostname format here.
_OCI_IMAGE_RE = re.compile(r"^oci-image:\s*(?P<image>.+?)\s*$")


class ExtendImageBuildPack(BuildPack):
    """A BuildPack that extends an existing base container image.

    Handles the common case of starting from a working base image and
    layering a small number of additional packages on top, e.g.::

        # runtime.txt
        oci-image:jupyter/scipy-notebook:2026-01-25

    ``runtime.txt`` must name the base image as ``oci-image:<image>[:<tag>]``.
    The image reference is passed through as-is, so any registry works:
    Docker Hub, GCR, GAR, ECR, ACR, or a self-hosted registry.

    Dependency installation (run as the image's existing user):

    * ``requirements.txt``  → ``python3 -m pip install -r requirements.txt``
    * ``environment.yml`` / ``environment.yaml`` → ``conda env update -n notebook``
    * ``install.R``         → ``Rscript install.R``
    """

    # Uses the shared Dockerfile template from BuildPack (self.template, set
    # in BuildPack.__init__). skip_base_setup=True below tells that template
    # to omit locale setup, user/group creation, and base apt package
    # installs, since the base image named in runtime.txt already provides
    # them. See the `{% if not skip_base_setup %}` guards in base.py.

    def __init__(self, base_image):
        super().__init__(base_image)
        self.skip_base_setup = True

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------

    def detect(self) -> bool:
        """Return True when ``runtime.txt`` specifies a base container image.

        ``__init__`` receives repo2docker's default ``base_image`` (e.g. the
        ``buildpack-deps`` image used by every other buildpack). We override
        ``self.base_image`` here, once we've confirmed ``runtime.txt`` names a
        recognised image reference, so ``render()`` emits ``FROM`` the image
        the repository actually asked for.
        """
        runtime_txt = self.binder_path("runtime.txt")
        if not os.path.isfile(runtime_txt):
            return False

        with open(runtime_txt) as f:
            content = f.read().strip()

        match = _OCI_IMAGE_RE.match(content)
        if not match:
            return False

        self.base_image = match.group("image")
        return True

    # ------------------------------------------------------------------
    # Build / assemble scripts
    # ------------------------------------------------------------------

    def _environment_file(self):
        """Path to the repo's environment.yml/environment.yaml, if any."""
        for candidate in ("environment.yml", "environment.yaml"):
            env_path = self.binder_path(candidate)
            if os.path.isfile(env_path):
                return env_path
        return None

    @lru_cache
    def get_preassemble_script_files(self) -> dict[str, str]:
        """Copy dependency files into the image before running install commands."""
        files = super().get_preassemble_script_files()

        apt_path = self.binder_path("apt.txt")
        if os.path.isfile(apt_path):
            files[apt_path] = "apt.txt"

        env_path = self._environment_file()
        if env_path is not None:
            # Normalize to a fixed name so get_preassemble_scripts() doesn't
            # need to care whether the repo used .yml or .yaml.
            files[env_path] = "environment.yml"

        req_path = self.binder_path("requirements.txt")
        if os.path.isfile(req_path):
            files[req_path] = req_path

        r_path = self.binder_path("install.R")
        if os.path.isfile(r_path):
            files[r_path] = r_path

        return files

    @lru_cache
    def get_preassemble_scripts(self) -> list[tuple[str, str]]:
        """Emit install commands for each recognised dependency file.

        Each command reads its dependency file (copied to ${REPO_DIR}, which
        is also the working directory at this point) at build time, inside
        the container's own shell.
        """
        scripts = super().get_preassemble_scripts()

        if os.path.isfile(self.binder_path("apt.txt")):
            scripts.append(
                (
                    "root",
                    r"""
                    apt-get update && \
                    apt-get install -y --no-install-recommends \
                        $(grep -v '^\s*#' apt.txt | grep -v '^\s*$' | tr -d '\r' | tr '\n' ' ') && \
                    apt-get clean && \
                    rm -rf /var/lib/apt/lists/* apt.txt
                    """,
                )
            )

        needs_user_context = (
            self._environment_file() is not None
            or os.path.isfile(self.binder_path("requirements.txt"))
            or os.path.isfile(self.binder_path("install.R"))
        )
        if needs_user_context:
            # The root-context steps above (and, on some build backends, the
            # underlying container runtime itself, e.g. emulating a
            # foreign-arch image) can leave root-owned files under $HOME.
            # Reclaim ownership before running anything as ${NB_USER}, or
            # those steps can fail with permission errors unrelated to the
            # repo's own dependency files.
            scripts.append(("root", "chown -R ${NB_USER}:${NB_USER} ${HOME}"))

        if self._environment_file() is not None:
            scripts.append(
                (
                    "${NB_USER}",
                    r"""
                    conda env update -n notebook -vvv -f environment.yml && \
                    conda clean -afy && rm -rf environment.yml ${HOME}/.cache/pip
                    """,
                )
            )

        if os.path.isfile(self.binder_path("requirements.txt")):
            scripts.append(
                (
                    "${NB_USER}",
                    r"""
                    python3 -m pip install --no-cache-dir -r requirements.txt && \
                    rm -rf requirements.txt
                    """,
                )
            )

        if os.path.isfile(self.binder_path("install.R")):
            scripts.append(
                (
                    "${NB_USER}",
                    r"Rscript install.R && rm -rf install.R",
                )
            )

        return scripts
