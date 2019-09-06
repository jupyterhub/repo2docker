"""
Test tarball loading and saving
"""

import os
import re
import docker
import pytest
import logging
from unittest.mock import MagicMock

from repo2docker.utils import chdir
from repo2docker.app import Repo2Docker
from repo2docker.buildpacks import TarballBuildPack


def create_test_tarball():
    # Run `repo2docker tests/base/node10`
    r2d = Repo2Docker(
        repo="tests/base/node10",
        user_id=os.geteuid(),
        user_name=os.getlogin(),
        #all_ports=all_ports,
        ports={},
        run=False,
    )
    r2d.build()

    client = docker.APIClient(version="auto")
    image = client.get_image(r2d.output_image_spec)
    with open('tests/tarball/node10/image.tar', 'wb') as f:
        for chunk in image:
            f.write(chunk)
        f.close()

def test_image_loading_image_name():
    if not os.path.isfile("tests/tarball/node10/image.tar"):
        create_test_tarball()
    
    r2d = Repo2Docker(
        repo="tests/tarball/node10", # will not match image name/tag below
        run=False,
    )

    r2d.initialize()
    r2d.build()
    
    assert re.match("r2dtests-2fbase-2fnode(.*):latest", r2d.output_image_spec)


def test_image_loading_error():
    r2d = Repo2Docker(
        repo="tests/tarball/empty_tar",
        run=False,
    )

    r2d.initialize()

    with pytest.raises(docker.errors.ImageLoadError, match = r".* no such file .*"):
        r2d.build()
     

def test_build_response():
    if not os.path.isfile("tests/tarball/node10/image.tar"):
        create_test_tarball()

    with chdir("tests/tarball/node10"):
        client = docker.APIClient(version="auto")
        
        result = TarballBuildPack().build(
            client, "whaterver-image", None, None, None, None
        )

        assert "image" in result[0]
        assert re.match("r2dtests-2fbase-2fnode(.*):latest", result[0]["image"])


def test_version_mismatch_warning(caplog):
    if not os.path.isfile("tests/tarball/node10/image.tar"):
        create_test_tarball()

    with chdir("tests/tarball/node10"):  
        fake_log_value = {"stream": "Loaded image: r2dtestimage"}
        fake_client = MagicMock(spec=docker.APIClient)
        fake_client.load_image.return_value = iter([fake_log_value])
        fake_labels = {"Config": { "Labels": { "repo2docker.version": "1.17.42" } } }
        fake_client.inspect_image.return_value = fake_labels
        
        with caplog.at_level(logging.INFO):
            result = TarballBuildPack().build(
                fake_client, "will-be-ignored-image", None, None, None, None
            )

            assert "repo2docker version missmatch" in str(caplog.text)
