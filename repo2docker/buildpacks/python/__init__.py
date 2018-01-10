"""
Generates a variety of Dockerfiles based on an input matrix
"""
from traitlets import default, Unicode, List
import os
from ..base import BuildPack


class PythonBuildPack(BuildPack):
    """
    """
    name = "python"
    version = "0.1"

    packages = {}

    path = [
        "${PYENV_ROOT}/shims",
        "${PYENV_ROOT}/bin",
        "${PYENV_ROOT}/versions/${BASE_PYENV}/bin"
    ]

    default_version = Unicode(
        '3.6.4',
        help="""
        The default python version to install with pyvenv.

        This *must* be a version that can install a new enough version of
        the notebook package.
        """
    )

    base_install_scripts = List(
        [],
        help="""
        Ordered list of shell script snippets to install base notebook.

        This should install the base python environment and appropriate
        required notebook packages.
        """
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            with open(self.binder_path('runtime.txt')) as f:
                runtime = f.read().strip()
                self.version = runtime.replace('python-', '')
        except FileNotFoundError:
            self.version = self.default_version

        # If 2.7 is specified, use 2.7.14, which is latest as of now.
        # This gets some crucial HTTPS fixes.
        if self.version == '2.7':
            self.version = '2.7.14'


    def compose_with(self, other):
        result = super().compose_with(other)
        result.default_version = self.default_version
        result.base_install_scripts = self.base_install_scripts

    @default('env')
    def setup_env(self):
        return [
            ("PYENV_ROOT", "${APP_BASE}/pyenv"),
            ("BASE_PYENV", self.default_version),
            # Prefix to use for installing kernels and finding jupyter binary
            ("NB_PYTHON_PREFIX", "${PYENV_ROOT}/versions/${BASE_PYENV}"),
            ("PYENV_VERSION", self.version)
        ]

    @default('build_scripts')
    def setup_build_script(self):
        build_scripts = [
                (
                    "root",
                    r"""
                    mkdir -p ${PYENV_ROOT} && \
                    chown -R ${NB_USER}:${NB_USER} ${PYENV_ROOT}
                    """
                ),
                (
                    "${NB_USER}",
                    r"""
                    git clone https://github.com/pyenv/pyenv.git $PYENV_ROOT && \
                    pyenv install ${BASE_PYENV}
                    """
                ),
            ] + self.base_install_scripts

        return build_scripts



    def detect(self):
        return os.path.exists('requirements.txt') and super().detect()


class PythonPipBuildPack(PythonBuildPack):
    whitelisted_base_versions = List(
        [
            '3.5.0',
            '3.5.1',
            '3.5.2',
            '3.5.3',
            '3.5.4',
            '3.6.0',
            '3.6.1',
            '3.6.2',
            '3.6.3',
            '3.6.4',
            'pypy3.5-5.9.0',
            'pypy3.5-5.8.0'
        ],
        help="""
        List of python versions that can be used for base environment.

        These must be able to support all the packages in requirements.frozen.txt.
        List is a whitelist from output of `pyenv install --list`.
        """
    )

    build_script_files = {
        'python/base.requirements.frozen.txt': '/tmp/base.requirements.frozen.txt',
        'python/kernel.requirements.frozen.txt': '/tmp/kernel.requirements.frozen.txt',
        'python/kernel.requirements2.frozen.txt': '/tmp/kernel.requirements2.frozen.txt',
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.version in self.whitelisted_base_versions:
            self.default_version = self.version

    @default('assemble_scripts')
    def setup_assemble_scripts(self):
        assemble_scripts = []
        if os.path.exists(self.binder_path('requirements.txt')):
            assemble_scripts += [(
                '${NB_USER}',
                'python -m pip install --no-cache-dir -r "{}"'.format(self.binder_path('requirements.txt'))
            )]

        if (os.path.exists(self.binder_path('requirements3.txt')) and
            self.version.startswith('2')):
            assemble_scripts += [(
                '${NB_USER}',
                'PYENV_VERSION=${BASE_PYENV} python -m pip install --no-cache-dir "{}"'.format(self.binder_path('requirements3.txt'))
            )]
        return assemble_scripts

    @default('base_install_scripts')
    def setup_base_install_scripts(self):
        base_install_scripts = [
            (
                "${NB_USER}",
                r"""
                PYENV_VERSION=${BASE_PYENV} \
                python -m pip install --no-cache-dir -r /tmp/base.requirements.frozen.txt && \
                PYENV_VERSION=${BASE_PYENV} \
                jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
                PYENV_VERSION=${BASE_PYENV} \
                jupyter serverextension enable --py jupyterlab --sys-prefix
                """
            )
        ]

        if self.version != self.default_version:
            # If we need to create an additional environment...
            base_requirements = '/tmp/kernel.requirements{}.frozen.txt'.format(
                '2' if self.version.startswith('2') else ''
            )

            base_install_scripts += [
                (
                    '${NB_USER}',
                    'pyenv install {}'.format(self.version)
                ),
                (
                    '${NB_USER}',
                    # Explicitly install a pinned version of pip,
                    # since lots of versions have an old version of pip.
                    'python -m pip install pip==9.0.1',
                ),
                (
                    '${NB_USER}',
                    'python -m pip install --no-cache-dir -r {}'.format(
                        base_requirements
                    )
                )
            ]

        return base_install_scripts
