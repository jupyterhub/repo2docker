from tempfile import TemporaryDirectory
from unittest.mock import patch

import docker
import escapism

from repo2docker.app import Repo2Docker
from repo2docker.__main__ import make_r2d


def test_find_image():
    images = [{'RepoTags': ['some-org/some-repo:latest']}]

    with patch('repo2docker.app.docker.APIClient') as FakeDockerClient:
        instance = FakeDockerClient.return_value
        instance.images.return_value = images

        r2d = Repo2Docker()
        r2d.output_image_spec = 'some-org/some-repo'
        assert r2d.find_image()

        instance.images.assert_called_with()


def test_dont_find_image():
    images = [{'RepoTags': ['some-org/some-image-name:latest']}]

    with patch('repo2docker.app.docker.APIClient') as FakeDockerClient:
        instance = FakeDockerClient.return_value
        instance.images.return_value = images

        r2d = Repo2Docker()
        r2d.output_image_spec = 'some-org/some-other-image-name'
        assert not r2d.find_image()

        instance.images.assert_called_with()


def test_image_name_remains_unchanged():
    # if we specify an image name, it should remain unmodified
    with TemporaryDirectory() as src:
        app = Repo2Docker()
        argv = ['--image-name', 'a-special-name', '--no-build', src]
        app = make_r2d(argv)

        app.start()

        assert app.output_image_spec == 'a-special-name'


def test_image_name_contains_sha1(repo_with_content):
    upstream, sha1 = repo_with_content
    app = Repo2Docker()
    # force selection of the git content provider by prefixing path with
    # file://. This is important as the Local content provider does not
    # store the SHA1 in the repo spec
    argv = ['--no-build', 'file://' + upstream]
    app = make_r2d(argv)

    app.start()

    assert app.output_image_spec.endswith(sha1[:7])


def test_local_dir_image_name(repo_with_content):
    upstream, sha1 = repo_with_content
    app = Repo2Docker()
    argv = ['--no-build', upstream]
    app = make_r2d(argv)

    app.start()

    assert app.output_image_spec.startswith(
        'r2d' + escapism.escape(upstream, escape_char='-').lower()
    )


def test_build_kwargs(repo_with_content):
    upstream, sha1 = repo_with_content
    argv = [upstream]
    app = make_r2d(argv)
    app.extra_build_kwargs = {'somekey': "somevalue"}

    with patch.object(docker.APIClient, 'build') as builds:
        builds.return_value = []
        app.build()
    builds.assert_called_once()
    args, kwargs = builds.call_args
    assert 'somekey' in kwargs
    assert kwargs['somekey'] == "somevalue"


def test_run_kwargs(repo_with_content):
    upstream, sha1 = repo_with_content
    argv = [upstream]
    app = make_r2d(argv)
    app.extra_run_kwargs = {'somekey': "somevalue"}

    with patch.object(docker.DockerClient, 'containers') as containers:
        app.start_container()
    containers.run.assert_called_once()
    args, kwargs = containers.run.call_args
    assert 'somekey' in kwargs
    assert kwargs['somekey'] == "somevalue"


def test_default_build(repo_with_content): 
    upstream, sha1 = repo_with_content
    argv = [upstream]
    app = make_r2d(argv)
    
    # some build should be called when --no-default-built is given. 
    with patch.object(docker.APIClient, 'build') as builds:
        builds.return_value = []
        image_built = app.build()
    builds.assert_called_once()
    assert image_built


def test_no_default_build(repo_with_content):
    upstream, sha1 = repo_with_content
    argv = ['--no-default-build', upstream]
    app = make_r2d(argv)

    # no default build for the empty repo
    with patch.object(docker.APIClient, 'build') as builds:
        builds.return_value = []
        image_built = app.build()
    assert not builds.called
    assert not image_built