"""
Custom test collector for our integration tests.

Each directory that has a script named 'verify' is considered
a test. jupyter-repo2docker is run on that directory,
and then ./verify is run inside the built container. It should
return a non-zero exit code for the test to be considered a
success.
"""

import os
import shlex

import pytest
import yaml

from repo2docker.app import Repo2Docker


def pytest_collect_file(parent, path):
    if path.basename == 'verify':
        return LocalRepo(path, parent)
    elif path.basename.endswith('.repos.yaml'):
        return RemoteRepoList(path, parent)


def make_test_func(args):
    """Generate a test function that runs repo2docker"""
    def test():
        app = Repo2Docker()
        app.initialize(args)
        app.start()
    return test


class Repo2DockerTest(pytest.Function):
    """A pytest.Item for running repo2docker"""
    def __init__(self, name, parent, args):
        f = parent.obj = make_test_func(args)
        super().__init__(name, parent, callobj=f)
        self.save_cwd = os.getcwd()

    def reportinfo(self):
        return self.parent.fspath, None, ""

    def teardown(self):
        super().teardown()
        os.chdir(self.save_cwd)


class LocalRepo(pytest.File):
    def collect(self):
        yield Repo2DockerTest(
            self.fspath.basename, self,
            args=[self.fspath.dirname, './verify'],
        )


class RemoteRepoList(pytest.File):
    def collect(self):
        with self.fspath.open() as f:
            repos = yaml.safe_load(f)
        for repo in repos:
            yield Repo2DockerTest(
                repo['name'], self,
                args=[
                    '--ref', repo['ref'],
                    repo['url'],
                    '--',
                ] + shlex.split(repo['verify']),
            )
