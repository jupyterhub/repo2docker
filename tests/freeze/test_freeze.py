"""test refreezing base environment"""

import os
from subprocess import check_output

import pytest
from repo2docker.buildpacks import conda
from repo2docker.buildpacks.conda import freeze

from repo2docker.utils import chdir

conda_dir = os.path.dirname(conda.__file__)


@pytest.mark.parametrize('py', ['2.7', '3.6'])
def test_freeze(capsys, py):
    with chdir(conda_dir):
        freeze.main(py)
        out = check_output(['git', 'diff'], cwd=conda_dir)
    with capsys.disabled():
        print(out.decode())
