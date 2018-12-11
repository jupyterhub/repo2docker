"""
Test that --cache-from is passed in to docker API properly.
"""
import os
import docker
from unittest.mock import MagicMock, patch
from repo2docker.buildpacks import BaseImage, DockerBuildPack, LegacyBinderDockerBuildPack
from tempfile import TemporaryDirectory

def test_cache_from_base(monkeypatch):
    FakeDockerClient = MagicMock()
    cache_from = [
        'image-1:latest'
    ]
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with TemporaryDirectory() as d:
        # Test base image build pack
        monkeypatch.chdir(d)
        for line in BaseImage().build(fake_client, 'image-2', '1Gi', {}, cache_from):
            assert line == fake_log_value
        called_args, called_kwargs = fake_client.build.call_args
        assert 'cache_from' in called_kwargs
        assert called_kwargs['cache_from'] == cache_from



def test_cache_from_docker(monkeypatch):
    FakeDockerClient = MagicMock()
    cache_from = [
        'image-1:latest'
    ]
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with TemporaryDirectory() as d:
        # Test docker image
        with open(os.path.join(d, 'Dockerfile'), 'w') as f:
            f.write('FROM scratch\n')

        for line in DockerBuildPack().build(fake_client, 'image-2', '1Gi', {}, cache_from):
            assert line == fake_log_value
        called_args, called_kwargs = fake_client.build.call_args
        assert 'cache_from' in called_kwargs
        assert called_kwargs['cache_from'] == cache_from

        # Test legacy docker image
        with open(os.path.join(d, 'Dockerfile'), 'w') as f:
            f.write('FROM andrewosh/binder-base\n')

        for line in LegacyBinderDockerBuildPack().build(fake_client, 'image-2', '1Gi', {}, cache_from):
            print(line)
            assert line == fake_log_value
        called_args, called_kwargs = fake_client.build.call_args
        assert 'cache_from' in called_kwargs
        assert called_kwargs['cache_from'] == cache_from


def test_cache_from_legacy(monkeypatch):
    FakeDockerClient = MagicMock()
    cache_from = [
        'image-1:latest'
    ]
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with TemporaryDirectory() as d:
        # Test legacy docker image
        with open(os.path.join(d, 'Dockerfile'), 'w') as f:
            f.write('FROM andrewosh/binder-base\n')

        for line in LegacyBinderDockerBuildPack().build(fake_client, 'image-2', '1Gi', {}, cache_from):
            assert line == fake_log_value
        called_args, called_kwargs = fake_client.build.call_args
        assert 'cache_from' in called_kwargs
        assert called_kwargs['cache_from'] == cache_from


