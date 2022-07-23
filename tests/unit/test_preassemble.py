import os

import pytest

from repo2docker import buildpacks


@pytest.mark.parametrize("binder_dir", ["", ".binder", "binder"])
def test_combine_preassemble_steps(tmpdir, binder_dir, base_image):
    tmpdir.chdir()
    if binder_dir:
        os.mkdir(binder_dir)

    # create two empty files for the build pack to use for pre-assembly
    open(os.path.join(binder_dir, "requirements.txt"), "w").close()
    open(os.path.join(binder_dir, "install.R"), "w").close()

    # trigger R build pack detection
    with open(os.path.join(binder_dir, "runtime.txt"), "w") as f:
        f.write("r-2019-01-30")

    bp = buildpacks.RBuildPack(base_image)
    files = bp.get_preassemble_script_files()

    assert len(files) == 2
    assert os.path.join(binder_dir, "requirements.txt") in files
    assert os.path.join(binder_dir, "install.R") in files
