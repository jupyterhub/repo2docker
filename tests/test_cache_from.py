"""
Test that --cache-from is passed in to docker API properly.
"""
import os
import docker
from unittest.mock import MagicMock, patch
from tempfile import TemporaryDirectory

def test_cache_from(monkeypatch):
    FakeDockerClient = MagicMock()
    cache_from = [
        'image-1:latest'
    ]
    fake_client = MagicMock(spec=docker.APIClient)
    fake_client.build.return_value = iter([{'stream': 'fake'}])

    with TemporaryDirectory() as d:
        monkeypatch.chdir(d)
        from repo2docker.buildpacks import BaseImage
        for line in BaseImage().build(fake_client, 'image-2', '1Gi', {}, cache_from):
            assert line == {'stream': 'fake'}
        called_args, called_kwargs = fake_client.build.call_args
        assert 'cache_from' in called_kwargs
        assert called_kwargs['cache_from'] == cache_from