"""
Test if the environment.yml is empty or it constains other data structure than a dictionary
"""
import os
import sys
import pytest
from repo2docker import buildpacks

#@pytest.mark.xfail(reason="Not yet implemented")
def test_empty_env_yml(tmpdir):
    tmpdir.chdir()
    p = tmpdir.join("environment.yml")
    bp = buildpacks.CondaBuildPack()
    with pytest.raises(Exception):
        py_ver = bp.python_version()

def test_no_dict_env_yml(tmpdir):
    tmpdir.chdir()
    q = tmpdir.join("environment.yml")
    q.write("list/n ,string")
    bq = buildpacks.CondaBuildPack()
    with pytest.raises(Exception):
        py_ver = bq.python_version()