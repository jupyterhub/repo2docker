"""
Tests for repo2docker/utils.py
"""
import traitlets
import os
from repo2docker import utils
import pytest
import subprocess
import tempfile


def test_capture_cmd_no_capture_success():
    # This should succeed
    for line in utils.execute_cmd(["/bin/bash", "-c", "echo test"]):
        pass


def test_capture_cmd_no_capture_fail():
    with pytest.raises(subprocess.CalledProcessError):
        for line in utils.execute_cmd(["/bin/bash", "-c", "e "]):
            pass


def test_capture_cmd_capture_success():
    # This should succeed
    for line in utils.execute_cmd(["/bin/bash", "-c", "echo test"], capture=True):
        assert line == "test\n"


def test_capture_cmd_noeol_capture_success():
    # This should succeed
    lines = list(
        utils.execute_cmd(["/bin/bash", "-c", "echo -en 'test\ntest'"], capture=True)
    )
    assert lines == ["test\n", "test"]


def test_capture_cmd_capture_fail():
    with pytest.raises(subprocess.CalledProcessError):
        for line in utils.execute_cmd(
            ["/bin/bash", "-c", "echo test; exit 1 "], capture=True
        ):
            assert line == "test\n"


def test_chdir(tmpdir):
    d = str(tmpdir.mkdir("cwd"))
    cur_cwd = os.getcwd()
    with utils.chdir(d):
        assert os.getcwd() == d
    assert os.getcwd() == cur_cwd


def test_byte_spec_validation():
    bs = utils.ByteSpecification()

    assert bs.validate(None, 1) == 1
    assert bs.validate(None, 1.0) == 1.0

    assert bs.validate(None, "1K") == 1024
    assert bs.validate(None, "1M") == 1024 * 1024
    assert bs.validate(None, "1G") == 1024 * 1024 * 1024
    assert bs.validate(None, "1T") == 1024 * 1024 * 1024 * 1024

    with pytest.raises(traitlets.TraitError):
        bs.validate(None, "NK")

    with pytest.raises(traitlets.TraitError):
        bs.validate(None, "1m")


@pytest.mark.parametrize(
    "input,expected",
    [
        (["8888:8888"], {"8888/tcp": "8888"}),
        (["8888:4321"], {"4321/tcp": "8888"}),
        (["8888:4321/udp"], {"4321/udp": "8888"}),
        (["8888:4321/udp", "8888:4321/tcp"], {"4321/udp": "8888", "4321/tcp": "8888"}),
        (["127.0.0.1:80:8000"], {"8000/tcp": ("127.0.0.1", "80")}),
        (["8888:4321", "1234:12345"], {"4321/tcp": "8888", "12345/tcp": "1234"}),
    ],
)
def test_valid_port_mapping(input, expected):
    actual = utils.validate_and_generate_port_mapping(input)
    assert actual == expected


@pytest.mark.parametrize("port_spec", ["a8888:8888", "888:888/abc"])
def test_invalid_port_mapping(port_spec):
    with pytest.raises(ValueError) as e:
        utils.validate_and_generate_port_mapping([port_spec])

    assert 'Port specification "{}"'.format(port_spec) in str(e.value)


def test_deep_get():
    data = {"data": {"files": [1, 2, 3]}}
    assert utils.deep_get(data, "data.files.0") == 1
    assert utils.deep_get(data, "data.files.1") == 2
    assert utils.deep_get(data, "data.files") == [1, 2, 3]
    assert utils.deep_get(data, "data") == {"files": [1, 2, 3]}


def test_is_doi():
    assert utils.is_doi("10.1234/jshd123") != None
    assert utils.is_doi("10.1234/JSHD.8192") != None
    assert utils.is_doi("doi.org/10.1234/jshd123") != None
    assert utils.is_doi("http://doi.org/10.1234/jshd123") != None
    assert utils.is_doi("https://doi.org/10.1234/jshd123") != None
    assert utils.is_doi("http://dx.doi.org/10.1234/jshd123") != None
    assert utils.is_doi("101234/jshd123") == None
    assert utils.is_doi("https://mybinder.org") == None


def test_normalize_doi():
    assert utils.normalize_doi("10.1234/jshd123") == "10.1234/jshd123"
    assert utils.normalize_doi("10.1234/JSHD.8192") == "10.1234/JSHD.8192"
    assert utils.normalize_doi("doi.org/10.1234/jshd123") == "10.1234/jshd123"
    assert utils.normalize_doi("http://doi.org/10.1234/jshd123") == "10.1234/jshd123"
    assert utils.normalize_doi("https://doi.org/10.1234/jshd123") == "10.1234/jshd123"
    assert utils.normalize_doi("http://dx.doi.org/10.1234/jshd123") == "10.1234/jshd123"


def test_open_guess_encoding():
    data = "Rică nu știa să zică râu, rățușcă, rămurică."
    with tempfile.NamedTemporaryFile(mode="wb") as test_file:
        test_file.write(str.encode(data, "utf-16"))
        test_file.seek(0)
        with utils.open_guess_encoding(test_file.name) as fd:
            assert fd.read() == data


@pytest.mark.parametrize(
    "req, is_local",
    [
        ("-r requirements.txt", True),
        ("-e .", True),
        ("--editable=.", True),
        (
            "--editable=git+https://github.com/popgensims/stdpopsim.git#egg=stdpopsim-master",
            False,
        ),
        ("file://subdir", True),
        ("file://./subdir", True),
        ("git://github.com/jupyterhub/repo2docker", False),
        ("git+https://github.com/jupyterhub/repo2docker", False),
        ("numpy", False),
        ("# -e .", False),
        ("--pre", False),
        # pip ignores the package name and treats this like `--pre` on a line
        # by itself
        ("--pre pandas", False),
        # These are invalid lines as far as pip is concerned, check that our
        # code is robust and continues running
        ("--unrecognized", False),
        ("-e", False),
    ],
)
def test_local_pip_requirement(req, is_local):
    assert utils.is_local_pip_requirement(req) == is_local
