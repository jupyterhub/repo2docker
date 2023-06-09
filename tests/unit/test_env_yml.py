"""
Test if the environment.yml is empty or it constains other data structure than a dictionary
"""

import pytest

from repo2docker import buildpacks


def test_empty_env_yml(tmpdir, base_image):
    tmpdir.chdir()
    p = tmpdir.join("environment.yml")
    p.write("")
    bp = buildpacks.CondaBuildPack(base_image)
    py_ver = bp.python_version
    # If the environment.yml is empty, python_version will get the default Python version
    assert py_ver == bp.major_pythons["3"]


def test_no_dict_env_yml(tmpdir, base_image):
    tmpdir.chdir()
    q = tmpdir.join("environment.yml")
    q.write("numpy\n " "matplotlib\n")
    bq = buildpacks.CondaBuildPack(base_image)
    with pytest.raises(TypeError):
        py_ver = bq.python_version
