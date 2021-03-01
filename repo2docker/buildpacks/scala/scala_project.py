"""Generates a Dockerfile based on an input matrix for Scala"""
import os
import toml
from ..python import PythonBuildPack
from .semver import find_semver_match


class ScalaBuildPack(PythonBuildPack):
    """
    Scala build pack which uses conda.
    """

    # ALL EXISTING SCALA VERSIONS
    # Note that these must remain ordered, in order for the find_semver_match()
    # function to behave correctly.
    all_scalas = [
        "2.12.12",
        "2.12.13",
        "2.13.4",
        "2.13.5"
    ]

    @property
    def scala_version(self):
        default_scala_version = self.all_scalas[-1]
        return default_scala_version

    def get_build_env(self):
        """Get additional environment settings for Scala and Jupyter

        Returns:
            an ordered list of environment setting tuples

            The tuples contain a string of the environment variable name and
            a string of the environment setting:
            - `SCALA_PATH`: base path where all Scala Binaries and libraries
                will be installed
            - `SCALA_DEPOT_PATH`: path where Scala libraries are installed.
            - `SCALA_VERSION`: default version of scala to be installed
            - `JUPYTER`: environment variable required by IScala to point to
                the `jupyter` executable

            For example, a tuple may be `('SCALA_VERSION', '2.13.5')`.

        """
        return super().get_build_env() + [
            ("SCALA_PATH", "${APP_BASE}/scala"),
            ("SCALA_BIN", "${SCALA_PATH}/bin"),
            ("COURSIER_CACHE", "${SCALA_PATH}/pkg"),
            ("COURSIER_BIN_DIR", "${SCALA_BIN}"),
            ("SCALA_VERSION", self.scala_version),
            ("JUPYTER", "${NB_PYTHON_PREFIX}/bin/jupyter"),
            ("JUPYTER_DATA_DIR", "${NB_PYTHON_PREFIX}/share/jupyter"),
        ]

    def get_env(self):
        return super().get_env() + [("SCALA_PROJECT", "${REPO_DIR}")]

    def get_path(self):
        """Adds path to Scala binaries to user's PATH.

        Returns:
            an ordered list of path strings. The path to the Scala
            executable is added to the list.

        """
        return super().get_path() + ["${SCALA_BIN}"]

    def get_build_scripts(self):
        """
        Return series of build-steps common to "ALL" Scala repositories

        All scripts found here should be independent of contents of a
        particular repository.

        This creates a directory with permissions for installing scala packages
        (from get_assemble_scripts).

        """
        return super().get_build_scripts() + [
            (
                "root",
                r"""
                mkdir -p ${SCALA_BIN} && \

                apt-get -y update && \
                    apt-get install --no-install-recommends -y \
                    curl \
                    openjdk-8-jre-headless \
                    ca-certificates-java && \
                    apt-get clean && \
                    rm -rf /var/lib/apt/lists/* && \

                curl -Lo ${SCALA_BIN}/coursier https://github.com/coursier/coursier/releases/download/v2.0.12/coursier && \
                chmod +x ${SCALA_BIN}/coursier
                """,
            ),
            (
                "root",
                r"""
                mkdir -p ${COURSIER_CACHE} && \
                chown ${NB_USER}:${NB_USER} ${COURSIER_CACHE}
                """,
            ),
        ]

    def get_assemble_scripts(self):
        """
        Return series of build-steps specific to "this" Scala repository

        We make sure that the IScala package gets installed into the default
        environment, and not the project specific one, by running the
        IScala install command with SCALA_PROJECT="".

        Instantiate and then precompile all packages in the repos scala
        environment.

        The parent, CondaBuildPack, will add the build steps for
        any needed Python packages found in environment.yml.
        """
        return super().get_assemble_scripts() + [
            (
                "${NB_USER}",
                r"""
                SCALA_PROJECT="" scala -e "using Pkg; Pkg.add(\"IScala\"); using IScala; installkernel(\"Scala\", \"--project=${REPO_DIR}\");" && \
                scala --project=${REPO_DIR} -e 'using Pkg; Pkg.instantiate(); Pkg.resolve(); pkg"precompile"'
                """,
            )
        ]

    def detect(self):
        """
        Check if current repo should be built with the Scala Build pack

        super().detect() is not called in this function - it would return
        false unless an `environment.yml` is present and we do not want to
        require the presence of a `environment.yml` to use Scala.

        Instead we just check if the path to `Project.toml` or
        `ScalaProject.toml` exists.

        """
        return os.path.exists(self.binder_path("build.sc")) or os.path.exists(
            self.binder_path("build.sbt")
        )
