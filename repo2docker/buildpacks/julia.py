"""
Generates a variety of Dockerfiles based on an input matrix
"""
import textwrap
from traitlets.config import LoggingConfigurable
from traitlets import Unicode, Set, List, Dict, Tuple, default
from textwrap import dedent
import jinja2
import tarfile
import io
import os
import stat
import re
import docker
from .base import BuildPack


class JuliaBuildPack(BuildPack):
    name = "julia"
    version = "0.1"
    env = [
        ('JULIA_PATH', '${APP_BASE}/julia'),
        ('JULIA_HOME', '${JULIA_PATH}/bin'),
        ('JULIA_PKGDIR', '${JULIA_PATH}/pkg'),
        ('JULIA_VERSION', '0.6.0'),
        ('JUPYTER', '${NB_PYTHON_PREFIX}/bin/jupyter')
    ]

    path = [
        '${JULIA_PATH}/bin'
    ]

    build_scripts = [
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
        (
            "${NB_USER}",
            # HACK: Can't seem to tell IJulia to install in sys-prefix
            # FIXME: Find way to get it to install under /srv and not $HOME?
            r"""
            julia -e 'Pkg.init(); Pkg.add("IJulia"); using IJulia;' && \
            mv ${HOME}/.local/share/jupyter/kernels/julia-0.6  ${NB_PYTHON_PREFIX}/share/jupyter/kernels/julia-0.6
            """
        )
    ]

    @default('assemble_scripts')
    def setup_assembly(self):
        require = self.binder_path('REQUIRE')
        return [(
            "${NB_USER}",
            # Pre-compile all libraries if they've opted into it. `using {libraryname}` does the
            # right thing
            r"""
            cat "%(require)s" >> ${JULIA_PKGDIR}/v0.6/REQUIRE && \
            julia -e ' \
               Pkg.resolve(); \
               for pkg in keys(Pkg.Reqs.parse("%(require)s")) \
                pkg != "julia" && eval(:(using $(Symbol(pkg)))) \
               end \
            '
            """ % { "require" : require }
        )]

    def detect(self):
        return os.path.exists(self.binder_path('REQUIRE')) and super()
