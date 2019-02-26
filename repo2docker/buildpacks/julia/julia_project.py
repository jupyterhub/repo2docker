"""Generates a Dockerfile based on an input matrix for Julia"""
import os
import toml
from .python import PythonBuildPack


class JuliaProjectTomlBuildPack(PythonBuildPack):
    """
    Julia build pack which uses conda.
    """

    minor_julias = {
        '1.0': '1.0.3',
        '1.1': '1.1.0',
    }
    major_julias = {
        '1': '1.1.0',
    }

    @property
    def julia_version(self):
        # TODO Read version out of the file
        # TODO Handle JuliaProject.toml
        project_toml = toml.load(self.binder_path('Project.toml'))
        if 'compat' in project_toml:
            if 'julia' in project_toml['compat']:
                return project_toml['compat']['julia']
        return self.major_julias['1']

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
                                  Similar to JULIA_PKGDIR, used in 1.0.
            - `JULIA_VERSION`: default version of julia to be installed
            - `JUPYTER`: environment variable required by IJulia to point to
                the `jupyter` executable

            For example, a tuple may be `('JULIA_VERSION', '0.6.0')`.

        """
        return super().get_build_env() + [
            ('JULIA_PATH', '${APP_BASE}/julia'),
            ('JULIA_HOME', '${JULIA_PATH}/bin'),  # julia <= 0.6
            ('JULIA_BINDIR', '${JULIA_HOME}'),  # julia >= 0.7
            ('JULIA_PKGDIR', '${JULIA_PATH}/pkg'),
            ('JULIA_DEPOT_PATH', '${JULIA_PKGDIR}'), # julia >= 0.7
            ('JULIA_VERSION', self.julia_version),
            ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter')
        ]

    def get_path(self):
        """Adds path to Julia binaries to user's PATH.

         Returns:
             an ordered list of path strings. The path to the Julia
             executable is added to the list.

        """
        return super().get_path() + ['${JULIA_HOME}']

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
                """
            ),
            (
                "root",
                r"""
                mkdir -p ${JULIA_PKGDIR} && \
                chown ${NB_USER}:${NB_USER} ${JULIA_PKGDIR}
                """
            ),
        ]            

    def get_assemble_scripts(self):
        """
        Return series of build-steps specific to "this" Julia repository

        Instantiate and then precompile all packages in the repos julia
        environment.
        
        The parent, CondaBuildPack, will add the build steps for
        any needed Python packages found in environment.yml.
        """
        return super().get_assemble_scripts() + [
            (
                "${NB_USER}",
                r"""
                julia -e "using Pkg; Pkg.add(\"IJulia\"); using IJulia; installkernel(\"Julia\", \"--project=${REPO_DIR}\", env=Dict(\"JUPYTER_DATA_DIR\"=>\"${NB_PYTHON_PREFIX}/share/jupyter\"));" && \
                julia --project=${REPO_DIR} -e 'using Pkg; Pkg.instantiate(); pkg"precompile"'
                """
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
        return os.path.exists(self.binder_path('Project.toml')) or os.path.exists(self.binder_path('JuliaProject.toml'))
