"""
tests to be run with pytest inside the container

can't be called test_whatever.py because then _host_ pytest will try to run it!
"""

import json
import os
import shutil
from subprocess import check_output

from pytest import fixture

kernel_prefix = os.environ.get("KERNEL_PYTHON_PREFIX")
server_prefix = os.environ.get("NB_PYTHON_PREFIX")


def json_cmd(cmd):
    """Run a command and decode its JSON output"""
    out = check_output(cmd)
    return json.loads(out.decode("utf8", "replace"))


def conda_pkgs(prefix):
    """Conda package list as a dict"""
    conda_json = json_cmd(["conda", "list", "--json", "-p", prefix])
    return {pkg["name"]: pkg for pkg in conda_json}


def pip_pkgs(prefix):
    """Pip package list as a dict"""
    pip_json = json_cmd([f"{prefix}/bin/pip", "list", "--format=json"])
    return {pkg["name"]: pkg for pkg in pip_json}


@fixture(scope="session")
def kernel_conda():
    return conda_pkgs(kernel_prefix)


@fixture(scope="session")
def server_conda():
    return conda_pkgs(server_prefix)


@fixture(scope="session")
def kernel_pip():
    return pip_pkgs(kernel_prefix)


@fixture(scope="session")
def server_pip():
    return pip_pkgs(server_prefix)


def test_which_python():
    # server python comes first. Is this expected?
    assert shutil.which("python3") == f"{server_prefix}/bin/python3"


def test_kernel_env(kernel_conda):
    assert kernel_prefix != server_prefix
    kernel_python = kernel_conda["python"]["version"]
    assert kernel_python[:3] == "3.6"
    # test environment.yml packages
    assert "numpy" in kernel_conda


def test_server_env(server_conda):
    # this should be the default version
    # it will need updating when the default changes
    assert server_conda["python"]["version"].split(".")[:2] == ["3", "10"]


def test_conda_install(kernel_conda, server_conda):
    # test that postBuild conda install went in the kernel env
    assert "make" in kernel_conda
    assert "make" not in server_conda


def test_pip_install(kernel_pip, server_pip):
    # server env comes first for pip
    # is this expected?
    assert "pytest" not in kernel_pip
    assert "pytest" in server_pip
