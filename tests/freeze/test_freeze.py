"""test refreezing base environment"""

import os
from subprocess import Popen, PIPE, STDOUT

import pytest
from repo2docker.buildpacks import conda
from repo2docker.buildpacks.conda import freeze

from repo2docker.utils import chdir

conda_dir = os.path.dirname(conda.__file__)


@pytest.mark.parametrize('py', ['2.7', '3.6'])
def test_freeze(capsys, py):
    with chdir(conda_dir):
        freeze.main(py)
        p = Popen(
            ['git', 'diff'],
            stdout=PIPE,
            stderr=STDOUT,
            cwd=conda_dir,
        )
        out, _ = p.communicate()
    with capsys.disabled():
        print(out.decode())
