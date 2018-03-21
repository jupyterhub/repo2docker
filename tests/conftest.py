"""Custom test collector for our integration tests.

Each directory in `tests` that has a script named 'verify' is considered
a test.

jupyter-repo2docker is run on that directory, and then ./verify is run inside
the built container. It should return a non-zero exit code for the test to be
considered a successful test.
"""

import os
import pipes
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
        self.args = args
        self.save_cwd = os.getcwd()
        f = parent.obj = make_test_func(args)
        super().__init__(name, parent, callobj=f)

    def reportinfo(self):
        return self.parent.fspath, None, ""

    def repr_failure(self, excinfo):
        err = excinfo.value
        if isinstance(err, SystemExit):
            cmd = "jupyter-repo2docker %s" % ' '.join(map(pipes.quote, self.args))
            return "%s | exited with status=%s" % (cmd, err.code)

        else:
            return super().repr_failure(excinfo)

    def teardown(self):
        super().teardown()
        os.chdir(self.save_cwd)


class LocalRepo(pytest.File):

    def collect(self):
        yield Repo2DockerTest(
            self.fspath.basename,
            self,
            args=[
                '--appendix',
                'RUN echo "appendix" > /tmp/appendix',
                self.fspath.dirname,
                './verify',
            ],
        )


class RemoteRepoList(pytest.File):

    def collect(self):
        with self.fspath.open() as f:
            repos = yaml.safe_load(f)
        for repo in repos:
            yield Repo2DockerTest(
                repo['name'],
                self,
                args=['--ref', repo['ref'], repo['url'], '--'] +
                shlex.split(repo['verify']),
            )
