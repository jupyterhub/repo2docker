"""Generates a Dockerfile based on an input matrix for Julia"""
import functools
import os
import requests
import toml
from ..python import PythonBuildPack
from .semver import find_semver_match, semver


class JuliaProjectTomlBuildPack(PythonBuildPack):
    """
    Julia build pack which uses conda.
    """

    # ALL EXISTING JULIA VERSIONS
    # Note that these must remain ordered, in order for the find_semver_match()
    # function to behave correctly.
    @property
    @functools.lru_cache(maxsize=1)
    def all_julias(self):
        try:
            json = requests.get(
                "https://julialang-s3.julialang.org/bin/versions.json"
            ).json()
        except Exception as e:
            raise RuntimeError("Failed to fetch available Julia versions: {e}")
        vers = [semver.VersionInfo.parse(v) for v in json.keys()]
        # filter out pre-release versions not supported by find_semver_match()
        filtered_vers = [v for v in vers if v.prerelease is None]
        # properly sort list of VersionInfo
        sorted_vers = sorted(
            filtered_vers, key=functools.cmp_to_key(semver.VersionInfo.compare)
        )
        # return list of semver string
        return [str(v) for v in sorted_vers]

    @property
    def julia_version(self):
        if os.path.exists(self.binder_path("JuliaProject.toml")):
            project_toml = toml.load(self.binder_path("JuliaProject.toml"))
        else:
            project_toml = toml.load(self.binder_path("Project.toml"))

        try:
            # For Project.toml files, install the latest julia version that
            # satisfies the given semver.
            compat = project_toml["compat"]["julia"]
        except:
            # Default version which needs to be manually updated with new major.minor releases
            compat = "1.5"

        match = find_semver_match(compat, self.all_julias)
        if match is None:
            raise RuntimeError("Failed to find a matching Julia version: {compat}")
        return match

    def get_build_env(self):
        """Get additional environment settings for Julia and Jupyter

        Returns:
            an ordered list of environment setting tuples

            The tuples contain a string of the environment variable name and
            a string of the environment setting:
            - `JULIA_PATH`: base path where all Julia Binaries and libraries
                will be installed
            - `JULIA_DEPOT_PATH`: path where Julia libraries are installed.
            - `JULIA_VERSION`: default version of julia to be installed
            - `JUPYTER`: environment variable required by IJulia to point to
                the `jupyter` executable

            For example, a tuple may be `('JULIA_VERSION', '0.6.0')`.

        """
        return super().get_build_env() + [
            ("JULIA_PATH", "${APP_BASE}/julia"),
            ("JULIA_DEPOT_PATH", "${JULIA_PATH}/pkg"),
            ("JULIA_VERSION", self.julia_version),
            ("JUPYTER", "${NB_PYTHON_PREFIX}/bin/jupyter"),
            ("JUPYTER_DATA_DIR", "${NB_PYTHON_PREFIX}/share/jupyter"),
        ]

    def get_env(self):
        return super().get_env() + [("JULIA_PROJECT", "${REPO_DIR}")]

    def get_path(self):
        """Adds path to Julia binaries to user's PATH.

        Returns:
            an ordered list of path strings. The path to the Julia
            executable is added to the list.

        """
        return super().get_path() + ["${JULIA_PATH}/bin"]

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
                mkdir -p ${JULIA_DEPOT_PATH} && \
                chown ${NB_USER}:${NB_USER} ${JULIA_DEPOT_PATH}
                """,
            ),
        ]

    def get_assemble_scripts(self):
        """
        Return series of build-steps specific to "this" Julia repository

        We make sure that the IJulia package gets installed into the default
        environment, and not the project specific one, by running the
        IJulia install command with JULIA_PROJECT="".

        Instantiate and then precompile all packages in the repos julia
        environment.

        The parent, CondaBuildPack, will add the build steps for
        any needed Python packages found in environment.yml.
        """
        return super().get_assemble_scripts() + [
            (
                "${NB_USER}",
                r"""
                JULIA_PROJECT="" julia -e "using Pkg; Pkg.add(\"IJulia\"); using IJulia; installkernel(\"Julia\", \"--project=${REPO_DIR}\");" && \
                julia --project=${REPO_DIR} -e 'using Pkg; Pkg.instantiate(); Pkg.resolve(); pkg"precompile"'
                """,
            )
        ]

    def detect(self):
        """
        Check if current repo should be built with the Julia Build pack

        super().detect() is not called in this function - it would return
        false unless an `environment.yml` is present and we do not want to
        require the presence of a `environment.yml` to use Julia.

        Instead we just check if the path to `Project.toml` or
        `JuliaProject.toml` exists.

        """
        return os.path.exists(self.binder_path("Project.toml")) or os.path.exists(
            self.binder_path("JuliaProject.toml")
        )
