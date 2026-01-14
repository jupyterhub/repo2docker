# this file is not called test_whatever
# so that the outer test discovery doesn't pick it up

import getpass
import os
import shutil
from pathlib import Path
from subprocess import check_output


def test_node():
    node = shutil.which("node")
    assert node is not None
    node_version = check_output(["node", "--version"], text=True)
    assert "v20" in node_version
    npm = shutil.which("npm")
    # npm version isn't pinned
    npm_version = check_output(["npm", "--version"], text=True)


def test_nb_user():
    assert os.getuid() == 1000
    assert os.getgid() == 1000
    user = getpass.getuser()
    assert user == "jovyan"
    home = Path.home()
    assert home == Path("/home/jovyan")
    assert home.exists()
    assert home.owner() == user
    with (home / "testfile").open("w") as f:
        f.write("canwrite")
    for p in home.rglob():
        assert p.owner() == user
