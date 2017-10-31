"""
Custom test collector for our integration tests.

Each directory that has a script named 'verify' is considered
a test. jupyter-repo2docker is run on that directory,
and then ./verify is run inside the built container. It should
return a non-zero exit code for the test to be considered a
success.
"""
import pytest
import os
import subprocess
import yaml
import shlex

def pytest_collect_file(parent, path):
    if path.basename == 'verify':
        return LocalRepo(path, parent)
    elif path.basename.endswith('.repos.yaml'):
        return RemoteRepoList(path, parent)

class LocalRepo(pytest.File):
    def collect(self):
        yield LocalRepoTest(self.fspath.basename, self, self.fspath)

class LocalRepoTest(pytest.Item):
    def __init__(self, name, parent, path):
        super().__init__(name, parent)
        self.path = path

    def runtest(self):
        readme_path = os.path.join(self.path.dirname, 'README.rst')
        if not os.path.exists(readme_path):
            raise Exception("README.rst required for test case in %s" % readme_path)
        subprocess.check_call([
            'jupyter-repo2docker',
            str(self.path.dirname),
            './verify'
        ])


class RemoteRepoList(pytest.File):
    def collect(self):
        with self.fspath.open() as f:
            repos = yaml.safe_load(f)
        for repo in repos:
            yield RemoteRepoTest(repo['name'], self, repo['url'], repo['ref'], repo['verify'])


class RemoteRepoTest(pytest.Item):
    def __init__(self, name, parent, url, ref, verify):
        super().__init__(name, parent)
        self.url = url
        self.ref = ref
        self.verify = verify

    def runtest(self):
        subprocess.check_call([
            'jupyter-repo2docker',
            '--ref', self.ref,
            self.url,
            '--',
        ] + shlex.split(self.verify))
