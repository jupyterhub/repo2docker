from datetime import date

import pytest
from requests.models import Response
from unittest.mock import patch

from repo2docker import buildpacks


def test_unsupported_version(tmpdir):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write("r-3.8-2019-01-01")

    r = buildpacks.RBuildPack()
    with pytest.raises(ValueError) as excinfo:
        # access the property to trigger the exception
        _ = r.r_version
        # check the version is mentioned in the exception
        assert "'3.8'" in str(excinfo.value)


@pytest.mark.parametrize(
    "runtime_version, expected", [("", "3.6"), ("3.6", "3.6"), ("3.5.1", "3.5")]
)
def test_version_specification(tmpdir, runtime_version, expected):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        if runtime_version:
            runtime_version += "-"
        f.write(f"r-{runtime_version}2019-01-01")

    r = buildpacks.RBuildPack()
    assert r.r_version.startswith(expected)


def test_version_completion(tmpdir):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write(f"r-3.6-2019-01-01")

    r = buildpacks.RBuildPack()
    assert r.r_version == "3.6.1-3bionic"


@pytest.mark.parametrize(
    "runtime, expected",
    [
        ("r-2019-01-01", (2019, 1, 1)),
        ("r-3.6.1-2019-01-01", (2019, 1, 1)),
        ("r-3.5-2019-01-01", (2019, 1, 1)),
    ],
)
def test_mran_date(tmpdir, runtime, expected):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write(runtime)

    r = buildpacks.RBuildPack()
    assert r.checkpoint_date == date(*expected)


@pytest.mark.parametrize("expected", ["2019-12-29", "2019-12-26"])
def test_mran_latestdate(tmpdir, expected):
    def mock_request_head(url):
        r = Response()
        if url == "https://mran.microsoft.com/snapshot/" + expected:
            r.status_code = 200
        else:
            r.status_code = 404
            r.reason = "Mock MRAN no snapshot"
        return r

    tmpdir.chdir()

    with open("DESCRIPTION", "w") as f:
        f.write("")

    with patch("requests.head", side_effect=mock_request_head):
        with patch("datetime.date") as mockdate:
            mockdate.today.return_value = date(2019, 12, 31)
            r = buildpacks.RBuildPack()
            r.detect()
    assert r.checkpoint_date.isoformat() == expected


def test_install_from_base(tmpdir):
    # check that for R==3.4 we install from ubuntu
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write("r-3.4-2019-01-02")

    r = buildpacks.RBuildPack()
    assert "r-base" in r.get_packages()


def test_install_from_ppa(tmpdir):
    # check that for R>3.4 we don't install r-base from Ubuntu
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write("r-3.5-2019-01-02")

    r = buildpacks.RBuildPack()
    assert "r-base" not in r.get_packages()


def test_custom_ppa(tmpdir):
    tmpdir.chdir()

    with open("runtime.txt", "w") as f:
        f.write("r-3.5-2019-01-02")

    r = buildpacks.RBuildPack()

    scripts = r.get_build_scripts()

    # check that at least one of the build scripts adds this new PPA
    for user, script in scripts:
        if "https://cloud.r-project.org/bin/linux/ubuntu bionic-cran35/" in script:
            break
    else:
        assert False, "Should have added a new PPA"

    # check that we install the right package
    for user, script in scripts:
        if "r-base=3.5" in script:
            break
    else:
        assert False, "Should have installed base R"
