import pytest
from repo2docker.utils import generate_repo_name


def test_generate_repo_name():
    reponame = 'github.com/jupyter/repo2docker'
    new_reponame = generate_repo_name(reponame, None)
    assert new_reponame == 'org-jupyter_repo-repo2docker_'

    new_reponame = generate_repo_name(reponame, 'test')
    assert new_reponame == 'org-jupyter_repo-repo2docker_ref-test_'

    reponame = 'foo.com/jupyter/repo2docker'
    new_reponame = generate_repo_name(reponame, 'test')
    assert new_reponame == reponame + '_'
