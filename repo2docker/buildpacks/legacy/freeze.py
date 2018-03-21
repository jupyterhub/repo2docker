#!/usr/bin/env python3
"""
Freeze the conda environment.yml for legacy dockerfiles.

It runs the freeze in the andrewosh/binder-base image used for legacy dockerfiles.

Usage:

python freeze.py [3.5]
"""

from datetime import datetime
import os
import pathlib
import shutil
from subprocess import check_call
import sys

# need conda ≥ 4.4 to avoid bug adding spurious pip dependencies
CONDA_VERSION = '4.4.11'

HERE = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))


def freeze(env_name, env_file, frozen_file):
    """Freeze a conda environment.yml

    By running in docker:

        conda env create
        conda env export

    Result will be stored in frozen_file
    """
    print(f"Freezing {env_file} -> {frozen_file}")

    with open(HERE / frozen_file, 'w') as f:
        f.write(f"# AUTO GENERATED FROM {env_file}, DO NOT MANUALLY MODIFY\n")
        f.write(f"# Frozen on {datetime.utcnow():%Y-%m-%d %H:%M:%S UTC}\n")

    check_call([
        'docker',
        'run',
        '--rm',
        '-v' f"{HERE}:/r2d",
        '-it',
        f"andrewosh/binder-base",
        "sh", "-c",
        '; '.join([
            "conda update -yq conda",
            f"conda install -yq conda={CONDA_VERSION}",
            'conda config --system --set auto_update_conda false',
            f"conda env update -f /r2d/{env_file} -n {env_name}",
            # exclude conda packages because we don't want to pin them
            f"conda env export -n {env_name} | grep -v conda >> /r2d/{frozen_file}",
        ])
    ])


if __name__ == '__main__':
    # allow specifying which env(s) to update on argv
    env_names = sys.argv[1:] or ('root', 'python3')
    for env_name in env_names:
        env_file = env_name + ".yml"
        frozen_file = os.path.splitext(env_file)[0] + '.frozen.yml'
        freeze(env_name, env_file, frozen_file)
