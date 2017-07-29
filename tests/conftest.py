"""
Custom test collector for our integration tests.

Each directory that has a script named 'verify' is considered
a test. jupyter-repo2docker is run on that directory,
and then ./verify is run inside the built container. It should
return a non-zero exit code for the test to be considered a
success.
"""
import pytest
import subprocess

def pytest_collect_file(parent, path):
    if path.basename == 'verify':
        return Repo(path, parent)

class Repo(pytest.File):
    def collect(self):
        yield RepoTest(self.fspath.basename, self, self.fspath)


class RepoTest(pytest.Item):
    def __init__(self, name, parent, path):
        super().__init__(name, parent)
        self.path = path

    def runtest(self):
        subprocess.check_call([
            'jupyter-repo2docker',
            str(self.path.dirname),
            './verify'
        ])
