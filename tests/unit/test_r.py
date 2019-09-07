from datetime import date

import pytest

from repo2docker import buildpacks


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
