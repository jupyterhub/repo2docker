#!/usr/bin/env python3
"""
Freeze the conda environment.yml

Run in a continuumio/miniconda3 image to ensure portability
"""

from datetime import datetime
import os
import pathlib
import shutil
from subprocess import check_call

from ruamel.yaml import YAML


MINICONDA_VERSION = '4.3.27'

HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = 'environment.yml'
FROZEN_FILE = os.path.splitext(ENV_FILE)[0] + '.frozen.yml'

ENV_FILE_T = 'environment.py-{py}.yml'
FROZEN_FILE_T = os.path.splitext(ENV_FILE_T)[0] + '.frozen.yml'

yaml = YAML(typ='rt')


def fixup(frozen_file):
    """Fixup a frozen environment file

    Conda export has a bug!
    https://github.com/conda/conda/pull/6391
    """
    with open(frozen_file) as f:
        env = yaml.load(f)

    # scrub spurious pip dependencies
    # due to conda #6391

    # note: this scrubs *all* pip dependencies,
    # so be more careful if we ever *want* conda to call
    # out to pip.
    pip_found = False
    for idx, dep in enumerate(env['dependencies']):
        if isinstance(dep, dict) and 'pip' in dep:
            pip_found = True
            break

    if pip_found:
        env['dependencies'].pop(idx)

    with open(frozen_file, 'w') as f:
        yaml.dump(env, f)


def freeze(env_file, frozen_file):
    """Freeze a conda environment.yml

    By running in docker:

        conda env create
        conda env export

    Result will be stored in frozen_file
    """

    with open(HERE / frozen_file, 'w') as f:
        f.write(f"# AUTO GENERATED FROM {env_file}, DO NOT MANUALLY MODIFY\n")
        f.write(f"# Frozen on {datetime.utcnow():%Y-%m-%d %H:%M:%S UTC}\n")

    check_call([
        'docker',
        'run',
        '--rm',
        '-v' f"{HERE}:/r2d",
        '-it',
        f"continuumio/miniconda3:{MINICONDA_VERSION}",
        "sh", "-c",
        '; '.join([
            'conda config --add channels conda-forge',
            'conda config --system --set auto_update_conda false',
            f"conda env create -v -f /r2d/{env_file} -n r2d",
            f"conda env export -n r2d >> /r2d/{frozen_file}",
        ])
    ])
    fixup(HERE / frozen_file)


def set_python(py_env_file, py):
    """Set the Python version in an env file"""
    if os.path.exists(py_env_file):
        # only clobber auto-generated files
        with open(py_env_file) as f:
            text = f.read()
            if text and 'GENERATED' not in text:
                return
    with open(ENV_FILE) as f:
        env = yaml.load(f)
    for idx, dep in enumerate(env['dependencies']):
        if dep.split('=')[0] == 'python':
            env['dependencies'][idx] = f'python={py}.*'
            break
    else:
        raise ValueError(f"python dependency not found in {env['dependencies']}")
    # update python dependency
    with open(py_env_file, 'w') as f:
        f.write(f"# AUTO GENERATED FROM {ENV_FILE}, DO NOT MANUALLY MODIFY\n")
        f.write(f"# Generated on {datetime.utcnow():%Y-%m-%d %H:%M:%S UTC}\n")
        yaml.dump(env, f)


if __name__ == '__main__':
    for py in ('2.7', '3.5', '3.6'):
        env_file = ENV_FILE_T.format(py=py)
        set_python(env_file, py)
        frozen_file = os.path.splitext(env_file)[0] + '.frozen.yml'
        freeze(env_file, frozen_file)
    # use last version as default
    shutil.copy(frozen_file, FROZEN_FILE)
