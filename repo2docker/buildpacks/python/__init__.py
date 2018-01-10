"""
Generates a variety of Dockerfiles based on an input matrix
"""
from traitlets import default
import os
from ..base import BuildPack


class PythonBuildPack(BuildPack):
    """
    """
    name = "python"
    version = "0.1"

    packages = {}


    build_script_files = {
        'python/requirements.frozen.txt': '/tmp/requirements.frozen.txt',
        'python/requirements2.frozen.txt': '/tmp/requirements2.frozen.txt',
    }

    path = [
        "${PYENV_ROOT}/shims",
        "${PYENV_ROOT}/bin",
        "${PYENV_ROOT}/versions/${DEFAULT_PYENV}/bin"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.default_version = '3.6.4'

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


    @default('env')
    def setup_env(self):
        return [
            ("PYENV_ROOT", "${APP_BASE}/pyenv"),
            ("VENV_PATH", "${APP_BASE}/venv"),
            ("DEFAULT_PYENV", self.default_version),
            # Prefix to use for installing kernels and finding jupyter binary
            ("NB_PYTHON_PREFIX", "${PYENV_ROOT}/versions/${DEFAULT_PYENV}"),
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
                    pyenv install ${DEFAULT_PYENV}
                    """
                ),
                (
                    "${NB_USER}",
                    r"""
                    PYENV_VERSION=${DEFAULT_PYENV} \
                    python -m pip install --no-cache-dir -r /tmp/requirements.frozen.txt && \
                    PYENV_VERSION=${DEFAULT_PYENV} \
                    jupyter nbextension enable --py widgetsnbextension --sys-prefix && \
                    PYENV_VERSION=${DEFAULT_PYENV} \
                    jupyter serverextension enable --py jupyterlab --sys-prefix
                    """
                )
            ]

        if self.version != self.default_version:
            base_requirements = '/tmp/requirements{}.frozen.txt'.format(
                '2' if self.version.startswith('2') else ''
            )

            build_scripts += [
                (
                    '${NB_USER}',
                    'pyenv install {}'.format(self.version)
                ),
            ]
        return build_scripts

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
                'PYENV_VERSION=${DEFAULT_PYENV} python -m pip install --no-cache-dir "{}"'.format(self.binder_path('requirements3.txt'))
            )]
        return assemble_scripts


    def detect(self):
        return os.path.exists('requirements.txt') and super().detect()
