import os

import pytest

from repo2docker.buildpacks import ExtendImageBuildPack


def _write(path, content=""):
    with open(path, "w") as f:
        f.write(content)


# ---------------------------------------------------------------------------
# detect()
# ---------------------------------------------------------------------------


def test_no_runtime_txt(tmpdir, base_image):
    tmpdir.chdir()
    bp = ExtendImageBuildPack(base_image)
    assert not bp.detect()


@pytest.mark.parametrize(
    "runtime_txt",
    [
        "python-3.11",
        "",
        "docker-image:jupyter/scipy-notebook:2026-01-25",
        "gcr.io/my-project/my-image:latest",
        "us-central1-docker.pkg.dev/my-project/my-repo/my-image:latest",
        "123456789012.dkr.ecr.us-east-1.amazonaws.com/my-image:latest",
    ],
)
def test_detect_rejects_non_oci_image_prefix(tmpdir, base_image, runtime_txt):
    tmpdir.chdir()
    _write("runtime.txt", runtime_txt)
    bp = ExtendImageBuildPack(base_image)
    assert not bp.detect()


def test_detect_oci_image(tmpdir, base_image):
    tmpdir.chdir()
    _write("runtime.txt", "oci-image:jupyter/scipy-notebook:2026-01-25")
    bp = ExtendImageBuildPack(base_image)
    assert bp.detect()
    assert bp.base_image == "jupyter/scipy-notebook:2026-01-25"


def test_detect_oci_image_strips_whitespace(tmpdir, base_image):
    tmpdir.chdir()
    _write("runtime.txt", "  oci-image:   jupyter/scipy-notebook:2026-01-25  \n")
    bp = ExtendImageBuildPack(base_image)
    assert bp.detect()
    assert bp.base_image == "jupyter/scipy-notebook:2026-01-25"


def test_detect_oci_image_custom_registry(tmpdir, base_image):
    tmpdir.chdir()
    ref = "us-central1-docker.pkg.dev/ucb-datahub-2018/base-images-repo/base-python-image:bb2e6c6"
    _write("runtime.txt", f"oci-image:{ref}")
    bp = ExtendImageBuildPack(base_image)
    assert bp.detect()
    assert bp.base_image == ref


def test_detect_sets_skip_base_setup(base_image):
    bp = ExtendImageBuildPack(base_image)
    assert bp.skip_base_setup is True


# ---------------------------------------------------------------------------
# get_preassemble_script_files()
# ---------------------------------------------------------------------------


def test_preassemble_script_files_empty(tmpdir, base_image):
    tmpdir.chdir()
    bp = ExtendImageBuildPack(base_image)
    assert bp.get_preassemble_script_files() == {}


def test_preassemble_script_files_all_present(tmpdir, base_image):
    tmpdir.chdir()
    _write("apt.txt")
    _write("environment.yml")
    _write("requirements.txt")
    _write("install.R")

    bp = ExtendImageBuildPack(base_image)
    files = bp.get_preassemble_script_files()

    assert files[os.path.join("", "apt.txt")] == "apt.txt"
    assert files[os.path.join("", "environment.yml")] == "environment.yml"
    assert files[os.path.join("", "requirements.txt")] == "requirements.txt"
    assert files[os.path.join("", "install.R")] == "install.R"


def test_preassemble_script_files_environment_yaml_normalized(tmpdir, base_image):
    tmpdir.chdir()
    _write("environment.yaml")

    bp = ExtendImageBuildPack(base_image)
    files = bp.get_preassemble_script_files()

    assert files[os.path.join("", "environment.yaml")] == "environment.yml"


def test_preassemble_script_files_prefers_yml_over_yaml(tmpdir, base_image):
    tmpdir.chdir()
    _write("environment.yml")
    _write("environment.yaml")

    bp = ExtendImageBuildPack(base_image)
    files = bp.get_preassemble_script_files()

    # only one environment file should be picked up, normalized to environment.yml
    env_sources = [src for src, dst in files.items() if dst == "environment.yml"]
    assert env_sources == [os.path.join("", "environment.yml")]


# ---------------------------------------------------------------------------
# get_preassemble_scripts()
# ---------------------------------------------------------------------------


def test_preassemble_scripts_empty(tmpdir, base_image):
    tmpdir.chdir()
    bp = ExtendImageBuildPack(base_image)
    assert bp.get_preassemble_scripts() == []


def test_preassemble_scripts_apt(tmpdir, base_image):
    tmpdir.chdir()
    _write("apt.txt")
    bp = ExtendImageBuildPack(base_image)
    scripts = bp.get_preassemble_scripts()

    assert len(scripts) == 1
    user, script = scripts[0]
    assert user == "root"
    assert "apt-get install" in script
    assert "apt.txt" in script


def test_preassemble_scripts_environment(tmpdir, base_image):
    tmpdir.chdir()
    _write("environment.yml")
    bp = ExtendImageBuildPack(base_image)
    scripts = bp.get_preassemble_scripts()

    # a "root" chown-fixup step precedes any step run as ${NB_USER}
    assert len(scripts) == 2
    assert scripts[0] == ("root", "chown -R ${NB_USER}:${NB_USER} ${HOME}")
    user, script = scripts[1]
    assert user == "${NB_USER}"
    assert "conda env update -n notebook" in script
    assert "environment.yml" in script


def test_preassemble_scripts_requirements(tmpdir, base_image):
    tmpdir.chdir()
    _write("requirements.txt")
    bp = ExtendImageBuildPack(base_image)
    scripts = bp.get_preassemble_scripts()

    assert len(scripts) == 2
    assert scripts[0] == ("root", "chown -R ${NB_USER}:${NB_USER} ${HOME}")
    user, script = scripts[1]
    assert user == "${NB_USER}"
    assert "pip install" in script
    assert "requirements.txt" in script


def test_preassemble_scripts_install_r(tmpdir, base_image):
    tmpdir.chdir()
    _write("install.R")
    bp = ExtendImageBuildPack(base_image)
    scripts = bp.get_preassemble_scripts()

    assert len(scripts) == 2
    assert scripts[0] == ("root", "chown -R ${NB_USER}:${NB_USER} ${HOME}")
    user, script = scripts[1]
    assert user == "${NB_USER}"
    assert "Rscript install.R" in script


def test_preassemble_scripts_order_all_present(tmpdir, base_image):
    tmpdir.chdir()
    _write("apt.txt")
    _write("environment.yml")
    _write("requirements.txt")
    _write("install.R")

    bp = ExtendImageBuildPack(base_image)
    scripts = bp.get_preassemble_scripts()

    assert len(scripts) == 5
    users = [user for user, _ in scripts]
    assert users == ["root", "root", "${NB_USER}", "${NB_USER}", "${NB_USER}"]
    assert scripts[1] == ("root", "chown -R ${NB_USER}:${NB_USER} ${HOME}")
