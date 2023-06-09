"""
Test that --cache-from is passed in to docker API properly.
"""

from unittest.mock import MagicMock

import docker
from repo2docker.buildpacks import (
    BaseImage,
    DockerBuildPack,
    LegacyBinderDockerBuildPack,
)


def test_cache_from_base(tmpdir, base_image):
    cache_from = ["image-1:latest"]
    fake_log_value = {"stream": "fake"}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])
    extra_build_kwargs = {"somekey": "somevalue"}

    # Test base image build pack
    tmpdir.chdir()
    for line in BaseImage(base_image).build(
        fake_client, "image-2", 100, {}, cache_from, extra_build_kwargs
    ):
        assert line == fake_log_value
    called_args, called_kwargs = fake_client.build.call_args
    assert "cache_from" in called_kwargs
    assert called_kwargs["cache_from"] == cache_from


def test_cache_from_docker(tmpdir, base_image):
    cache_from = ["image-1:latest"]
    fake_log_value = {"stream": "fake"}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])
    extra_build_kwargs = {"somekey": "somevalue"}
    tmpdir.chdir()

    # test dockerfile
    with tmpdir.join("Dockerfile").open("w") as f:
        f.write("FROM scratch\n")

    for line in DockerBuildPack(base_image).build(
        fake_client, "image-2", 100, {}, cache_from, extra_build_kwargs
    ):
        assert line == fake_log_value
    called_args, called_kwargs = fake_client.build.call_args
    assert "cache_from" in called_kwargs
    assert called_kwargs["cache_from"] == cache_from
