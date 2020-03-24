import os

import pytest

from repo2docker import buildpacks


@pytest.mark.parametrize("binder_dir", ["", ".binder", "binder"])
def test_pipfile_with_no_local_dependency_is_preassembled(tmpdir, binder_dir):
    tmpdir.chdir()
    if binder_dir:
        os.mkdir(binder_dir)

    with open(os.path.join(binder_dir, "Pipfile"), "w") as f:
        f.write(
            """
            [packages]
            there = "*"
            """
        )

    bp = buildpacks.PipfileBuildPack()
    assert bp._should_preassemble_pipenv == True


@pytest.mark.parametrize("binder_dir", ["", ".binder", "binder"])
def test_pipfile_with_local_dependency_is_not_preassembled(tmpdir, binder_dir):
    tmpdir.chdir()
    if binder_dir:
        os.mkdir(binder_dir)

    with open(os.path.join(binder_dir, "Pipfile"), "w") as f:
        f.write(
            """
            [packages]
            there = "*"
            dummy = {path=".", editable=true}
            """
        )

    bp = buildpacks.PipfileBuildPack()
    assert bp._should_preassemble_pipenv == False


@pytest.mark.parametrize("binder_dir", ["", ".binder", "binder"])
def test_lockfile_with_no_local_dependency_is_preassembled(tmpdir, binder_dir):
    tmpdir.chdir()
    if binder_dir:
        os.mkdir(binder_dir)

    with open(os.path.join(binder_dir, "Pipfile.lock"), "w") as f:
        f.write(
            """
            {
                "default": {
                    "pypi-pkg-test": {
                    }
                }
            }
            """
        )

    bp = buildpacks.PipfileBuildPack()
    assert bp._should_preassemble_pipenv == True


@pytest.mark.parametrize("binder_dir", ["", ".binder", "binder"])
def test_lockfile_with_local_dependency_is_not_preassembled(tmpdir, binder_dir):
    tmpdir.chdir()
    if binder_dir:
        os.mkdir(binder_dir)

    with open(os.path.join(binder_dir, "Pipfile.lock"), "w") as f:
        f.write(
            """
            {
                "default": {
                    "pypi-pkg-test": {
                        "path": "..."
                    }
                }
            }
            """
        )

    bp = buildpacks.PipfileBuildPack()
    assert bp._should_preassemble_pipenv == False
