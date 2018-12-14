"""
Test that build time memory limits are passed through to docker.

We don't have to actually test if the limit is respected,
since that is docker's job.
"""
import os
from unittest.mock import MagicMock
from tempfile import TemporaryDirectory
from repo2docker.buildpacks import BaseImage, DockerBuildPack, LegacyBinderDockerBuildPack
import docker


def test_memory_base(monkeypatch):
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with TemporaryDirectory() as d:
        # Test base image build pack
        monkeypatch.chdir(d)
        for line in BaseImage().build(fake_client, 'image-2', '1Gi', {}, []):
            assert line == fake_log_value
        _, called_kwargs = fake_client.build.call_args
        assert 'container_limits' in called_kwargs
        assert 'memory' in called_kwargs['container_limits']
        assert called_kwargs['container_limits']['memory'] == '1Gi'


def test_memory_docker(monkeypatch):
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with TemporaryDirectory() as d:
        # Test docker image
        with open(os.path.join(d, 'Dockerfile'), 'w') as f:
            f.write('FROM scratch\n')
        monkeypatch.chdir(d)
        for line in DockerBuildPack().build(fake_client, 'image-2', '1Gi', {}, []):
            assert line == fake_log_value
        _, called_kwargs = fake_client.build.call_args
        assert 'container_limits' in called_kwargs
        assert 'memory' in called_kwargs['container_limits']
        assert called_kwargs['container_limits']['memory'] == '1Gi'

def test_memory_legacy_docker(monkeypatch):
    fake_log_value = {'stream': 'fake'}
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([fake_log_value])

    with TemporaryDirectory() as d:
        monkeypatch.chdir(d)

        # Test legacy docker image
        with open(os.path.join(d, 'Dockerfile'), 'w') as f:
            f.write('FROM andrewosh/binder-base\n')

        for line in LegacyBinderDockerBuildPack().build(fake_client, 'image-2', '1Gi', {}, []):
            assert line == fake_log_value
        _, called_kwargs = fake_client.build.call_args
        assert 'container_limits' in called_kwargs
        assert 'memory' in called_kwargs['container_limits']
        assert called_kwargs['container_limits']['memory'] == '1Gi'
