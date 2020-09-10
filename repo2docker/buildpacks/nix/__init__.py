"""BuildPack for nixpkgs environments"""
import os

from ..base import BuildPack, BaseImage


class NixBuildPack(BaseImage):
    """A nix Package Manager BuildPack"""

    def get_path(self):
        """Return paths to be added to PATH environemnt variable"""
        return super().get_path() + ["/home/${NB_USER}/.nix-profile/bin"]

    def get_env(self):
        """Ordered list of environment variables to be set for this image"""
        return super().get_env() + [
            ("NIX_PATH", "nixpkgs=/home/${NB_USER}/.nix-defexpr/channels/nixpkgs"),
            ("NIX_SSL_CERT_FILE", "/etc/ssl/certs/ca-certificates.crt"),
            ("GIT_SSL_CAINFO", "/etc/ssl/certs/ca-certificates.crt"),
        ]

    def get_build_scripts(self):
        """
        Return series of build-steps common to all nix repositories.
        Notice how only root privileges are needed for creating nix
        directory.

         - create nix directory for user nix installation
         - install nix package manager for user
        """
        return super().get_build_scripts() + [
            (
                "root",
                """
            mkdir -m 0755 /nix && \
            chown -R ${NB_USER}:${NB_USER} /nix /usr/local/bin/nix-shell-wrapper /home/${NB_USER}
            """,
            ),
            (
                "${NB_USER}",
                """
            bash /home/${NB_USER}/.local/bin/install-nix.bash && \
            rm /home/${NB_USER}/.local/bin/install-nix.bash
            """,
            ),
        ]

    def get_build_script_files(self):
        """Dict of files to be copied to the container image for use in building"""
        return {
            "nix/install-nix.bash": "/home/${NB_USER}/.local/bin/install-nix.bash",
            "nix/nix-shell-wrapper": "/usr/local/bin/nix-shell-wrapper",
        }

    def get_assemble_scripts(self):
        """Return series of build-steps specific to this source repository."""
        return super().get_assemble_scripts() + [
            (
                "${NB_USER}",
                """
            nix-channel --add https://nixos.org/channels/nixpkgs-unstable nixpkgs && \
            nix-channel --update && \
            nix-shell {}
            """.format(
                    self.binder_path("default.nix")
                ),
            )
        ]

    def get_start_script(self):
        """The path to a script to be executed as ENTRYPOINT"""
        # the shell wrapper script duplicates the behaviour of other buildpacks
        # when it comes to the `start` script as well as handling a binder/
        # sub-directory when it exists
        return "/usr/local/bin/nix-shell-wrapper"

    def detect(self):
        """Check if current repo should be built with the nix BuildPack"""
        return os.path.exists(self.binder_path("default.nix"))
