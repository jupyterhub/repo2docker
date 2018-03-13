from contextlib import contextmanager
import shutil
import os
import subprocess
from tempfile import TemporaryDirectory
from repo2docker.contentproviders.git import GitContentProvider


@contextmanager
def git_repo():
    """
    Makes a dummy git repo in which user can perform git operations

    Should be used as a contextmanager, it will delete directory when done
    """

    with TemporaryDirectory() as gitdir:
        subprocess.check_call(['git', 'init'], cwd=gitdir)

        yield gitdir

def test_clone():
    """Test simple git clone to a target dir
    """
    with git_repo() as upstream:
        with open(os.path.join(upstream, 'test'), 'w') as f:
            f.write("Hello")

        subprocess.check_call(['git', 'add', 'test'], cwd=upstream)
        subprocess.check_call(['git', 'commit', '-m', 'Test commit'], cwd=upstream)

        with TemporaryDirectory() as clone_dir:
            spec = {
                'url': upstream
            }
            for _ in GitContentProvider().provide(spec, clone_dir, False):
                pass
            assert os.path.exists(os.path.join(clone_dir, 'test'))
