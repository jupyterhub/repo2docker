"""Generates a Dockerfile based on an input matrix with REQUIRE for legacy Julia"""

from distutils.version import LooseVersion as V
import os

from ..python import PythonBuildPack


class JuliaRequireBuildPack(PythonBuildPack):
    """
    Julia build pack which uses conda and REQUIRE.
    """

    minor_julias = {"0.6": "0.6.4", "0.7": "0.7.0", "1.0": "1.0.4", "1.1": "1.1.1"}
    major_julias = {"1": "1.1.1"}

    @property
    def python_version(self):
        # IJulia doesn't build on julia 0.6
        # due to old incompatibilities with Jupyter-core >= 4.5,
        # so use the similarly-old Python 3.5 base environment
        if V(self.julia_version) < V("0.7"):
            return "3.5"
        else:
            return super().python_version

    @property
    def julia_version(self):
        require = self.binder_path("REQUIRE")
        try:
            with open(require) as f:
                julia_version_line = (
                    f.readline().strip()
                )  # First line is optionally a julia version
        except FileNotFoundError:
            julia_version_line = ""

        if not julia_version_line.startswith("julia "):
            # not a Julia version line.
            # use the default Julia.
            self._julia_version = self.minor_julias["0.6"]
            return self._julia_version

        julia_version_info = julia_version_line.split(" ", 1)[1].split(".")
        julia_version = ""
        if len(julia_version_info) == 1:
            julia_version = self.major_julias[julia_version_info[0]]
        elif len(julia_version_info) == 2:
            # get major.minor
            julia_version = self.minor_julias[".".join(julia_version_info)]
        else:
            # use supplied julia version
            julia_version = ".".join(julia_version_info)
        self._julia_version = julia_version
        return self._julia_version

    def get_build_env(self):
        """Get additional environment settings for Julia and Jupyter

        Returns:
            an ordered list of environment setting tuples

            The tuples contain a string of the environment variable name and
            a string of the environment setting:
            - `JULIA_PATH`: base path where all Julia Binaries and libraries
                will be installed
            - `JULIA_HOME`: path where all Julia Binaries will be installed
            - `JULIA_PKGDIR`: path where all Julia libraries will be installed
            - `JULIA_DEPOT_PATH`: path where Julia libraries are installed.
                                  Similar to JULIA_PKGDIR, used in 1.x.
            - `JULIA_VERSION`: default version of julia to be installed
            - `JUPYTER`: environment variable required by IJulia to point to
                the `jupyter` executable

            For example, a tuple may be `('JULIA_VERSION', '0.6.0')`.

        """
        return super().get_build_env() + [
            ("JULIA_PATH", "${APP_BASE}/julia"),
            ("JULIA_HOME", "${JULIA_PATH}/bin"),  # julia <= 0.6
            ("JULIA_BINDIR", "${JULIA_HOME}"),  # julia >= 0.7
            ("JULIA_PKGDIR", "${JULIA_PATH}/pkg"),
            ("JULIA_DEPOT_PATH", "${JULIA_PKGDIR}"),  # julia >= 0.7
            ("JULIA_VERSION", self.julia_version),
            ("JUPYTER", "${NB_PYTHON_PREFIX}/bin/jupyter"),
        ]

    def get_path(self):
        """Adds path to Julia binaries to user's PATH.

        Returns:
            an ordered list of path strings. The path to the Julia
            executable is added to the list.

        """
        return super().get_path() + ["${JULIA_HOME}"]

    def get_build_scripts(self):
        """
        Return series of build-steps common to "ALL" Julia repositories

        All scripts found here should be independent of contents of a
        particular repository.

        This creates a directory with permissions for installing julia packages
        (from get_assemble_scripts).

        """
        return super().get_build_scripts() + [
            (
                "root",
                r"""
                mkdir -p ${JULIA_PATH} && \
                curl -sSL "https://julialang-s3.julialang.org/bin/linux/x64/${JULIA_VERSION%[.-]*}/julia-${JULIA_VERSION}-linux-x86_64.tar.gz" | tar -xz -C ${JULIA_PATH} --strip-components 1
                """,
            ),
            (
                "root",
                r"""
                mkdir -p ${JULIA_PKGDIR} && \
                chown ${NB_USER}:${NB_USER} ${JULIA_PKGDIR}
                """,
            ),
            (
                "${NB_USER}",
                # HACK: Can't seem to tell IJulia to install in sys-prefix
                # FIXME: Find way to get it to install under /srv and not $HOME?
                r"""
                julia -e 'if (VERSION > v"0.7-") using Pkg; else Pkg.init(); end; Pkg.add("IJulia"); using IJulia;' && \
                mv ${HOME}/.local/share/jupyter/kernels/julia-${JULIA_VERSION%[.-]*}  ${NB_PYTHON_PREFIX}/share/jupyter/kernels/julia-${JULIA_VERSION%[.-]*}
                """,
            ),
        ]

    def get_assemble_scripts(self):
        """
        Return series of build-steps specific to "this" Julia repository

        Precompile all Julia libraries found in the repository's REQUIRE
        file. The parent, CondaBuildPack, will add the build steps for
        any needed Python packages found in environment.yml.

        """
        require = self.binder_path("REQUIRE")
        return super().get_assemble_scripts() + [
            (
                "${NB_USER}",
                # Install and pre-compile all libraries if they've opted into it.
                # In v0.6, Pkg.resolve() installs all the packages, but in v0.7+, we
                # have to manually Pkg.add() each of them (since the REQUIRES file
                # format is deprecated).
                # The precompliation is done via `using {libraryname}`.
                r"""
            julia /tmp/install-repo-dependencies.jl "%(require)s"
            """
                % {"require": require}
                # TODO: For some reason, `rm`ing the file fails with permission denied.
                # && rm /tmp/install-repo-dependencies.jl
            )
        ]

    def get_build_script_files(self):
        files = {
            "julia/install-repo-dependencies.jl": "/tmp/install-repo-dependencies.jl"
        }
        files.update(super().get_build_script_files())
        return files

    def detect(self):
        """
        Check if current repo should be built with the Julia Legacy Build pack

        super().detect() is not called in this function - it would return
        false unless an `environment.yml` is present and we do not want to
        require the presence of a `environment.yml` to use Julia.

        Instead we just check if the path to `REQUIRE` exists and that there is
        no julia 1.0 style environment

        """
        return os.path.exists(self.binder_path("REQUIRE")) and not (
            os.path.exists(self.binder_path("Project.toml"))
            or os.path.exists(self.binder_path("JuliaProject.toml"))
        )
