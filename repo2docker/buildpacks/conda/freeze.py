#!/usr/bin/env python3
"""
Freeze the conda environment.yml

Run in a continuumio/miniconda3 image to ensure portability
"""

from datetime import datetime
import os
import pathlib
from subprocess import check_call

from ruamel.yaml import YAML


MINICONDA_VERSION = '4.3.27'

HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = 'environment.yml'
FROZEN_FILE = 'environment.frozen.yml'

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
            f"conda env export -n r2d > /r2d/{frozen_file}",
        ])
    ])
    fixup(HERE / frozen_file)


if __name__ == '__main__':
    freeze(ENV_FILE, FROZEN_FILE)
