"""
Custom test collector for our integration tests.


Test lifecycle:
- Find all directories that contain `verify` or `*.repos.yaml`
- If `verify` is found:
    - Run `jupyter-repo2docker` on the test directory.
      - Extra arguments may be added as YAML list of strings in `extra-args.yaml`.
    - Run `./verify` inside the built container.
    - It should return a non-zero exit code for the test to be considered a
      successful.
- If a `*.repos.yaml` is found:
    - For each entry of the form `{name, url, ref, verify}`
        - Run `jupyter-repo2docker` with the `url` and `ref`
        - Run the `verify` inside the built container
"""

import os
import shlex
import subprocess
import time
from tempfile import TemporaryDirectory

import escapism
import pytest
import requests
import yaml

from repo2docker.__main__ import make_r2d

TESTS_DIR = os.path.abspath(os.path.dirname(__file__))


def pytest_collect_file(parent, file_path):
    if file_path.name == "verify":
        return LocalRepo.from_parent(parent, path=file_path)
    elif file_path.name.endswith(".repos.yaml"):
        return RemoteRepoList.from_parent(parent, path=file_path)


def make_test_func(args, skip_build=False, extra_run_kwargs=None):
    """Generate a test function that runs repo2docker"""

    def test():
        app = make_r2d(args)
        app.initialize()
        if extra_run_kwargs:
            app.extra_run_kwargs.update(extra_run_kwargs)
        if skip_build:

            def build_noop():
                print("Skipping build")

            app.skip_build = build_noop
        if app.run_cmd:
            # verify test, run it
            app.start()
            return
        # no run_cmd given, starting notebook server
        app.run = False
        app.start()  # This just build the image and does not run it.
        container = app.start_container()
        port = app.port
        # wait a bit for the container to be ready
        container_url = f"http://localhost:{port}/api"
        # give the container a chance to start
        time.sleep(1)
        try:
            # try a few times to connect
            success = False
            for i in range(1, 4):
                container.reload()
                assert container.status == "running"
                try:
                    info = requests.get(container_url).json()
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(i * 3)
                else:
                    print(info)
                    success = True
                    break
            assert success, f"Notebook never started in {container}"
        finally:
            # stop the container
            container.stop()
            app.wait_for_container(container)

    return test


# Provide a fixture for testing in .py files
@pytest.fixture()
def run_repo2docker():
    def run_test(args):
        return make_test_func(args)()

    return run_test


@pytest.fixture()
def base_image():
    """
    Base ubuntu image to use when testing specific BuildPacks
    """
    return "buildpack-deps:jammy"


def _add_content_to_git(repo_dir):
    """Add content to file 'test' in git repository and commit."""
    # use append mode so this can be called multiple times
    with open(os.path.join(repo_dir, "test"), "a") as f:
        f.write("Hello")

    subprocess.check_call(["git", "add", "test"], cwd=repo_dir)
    subprocess.check_call(["git", "commit", "-m", "Test commit"], cwd=repo_dir)


def _get_sha1(repo_dir):
    """Get repository's current commit SHA1."""
    sha1 = subprocess.Popen(
        ["git", "rev-parse", "HEAD"], stdout=subprocess.PIPE, cwd=repo_dir
    )
    return sha1.stdout.read().decode().strip()


@pytest.fixture()
def git_repo():
    """
    Make a dummy git repo in which user can perform git operations

    Should be used as a contextmanager, it will delete directory when done
    """
    with TemporaryDirectory() as gitdir:
        subprocess.check_call(["git", "init"], cwd=gitdir)
        yield gitdir


@pytest.fixture()
def repo_with_content(git_repo):
    """Create a git repository with content"""
    _add_content_to_git(git_repo)
    sha1 = _get_sha1(git_repo)

    yield git_repo, sha1


@pytest.fixture
def repo_with_submodule():
    """Create a git repository with a git submodule in a non-master branch.

    Provides parent repository directory, current parent commit SHA1, and
    the submodule's current commit. The submodule will be added under the
    name "submod" in the parent repository.

    Creating the submodule in a separate branch is useful to prove that
    submodules are initialized properly when the master branch doesn't have
    the submodule yet.

    """
    submodule_repo = "https://github.com/binderhub-ci-repos/requirements"
    submod_sha1_b = "20c4fe55a9b2c5011d228545e821b1c7b1723652"

    with TemporaryDirectory() as git_a_dir:
        # create "parent" repository
        subprocess.check_call(["git", "init"], cwd=git_a_dir)
        _add_content_to_git(git_a_dir)

        # create a new branch in the parent without any submodule
        subprocess.check_call(
            ["git", "checkout", "-b", "branch-without-submod"], cwd=git_a_dir
        )
        # create a new branch in the parent to add the submodule
        subprocess.check_call(
            ["git", "checkout", "-b", "branch-with-submod"], cwd=git_a_dir
        )
        subprocess.check_call(
            [
                "git",
                "submodule",
                "add",
                submodule_repo,
                "submod",
            ],
            cwd=git_a_dir,
        )
        # checkout the first commit for the submod, not the latest
        subprocess.check_call(
            ["git", "checkout", submod_sha1_b], cwd=os.path.join(git_a_dir, "submod")
        )
        subprocess.check_call(["git", "add", git_a_dir, ".gitmodules"], cwd=git_a_dir)
        subprocess.check_call(
            ["git", "commit", "-m", "Add B repos submod"], cwd=git_a_dir
        )

        sha1_a = _get_sha1(git_a_dir)
        yield git_a_dir, sha1_a, submod_sha1_b


class Repo2DockerTest(pytest.Function):
    """A pytest.Item for running repo2docker"""

    def __init__(
        self, name, parent, args=None, skip_build=False, extra_run_kwargs=None
    ):
        self.args = args
        self.save_cwd = os.getcwd()
        f = parent.obj = make_test_func(
            args, skip_build=skip_build, extra_run_kwargs=extra_run_kwargs
        )
        super().__init__(name, parent, callobj=f)

    def reportinfo(self):
        return (self.parent.path, None, "")

    def repr_failure(self, excinfo):
        err = excinfo.value
        if isinstance(err, SystemExit):
            cmd = f'jupyter-repo2docker {" ".join(map(shlex.quote, self.args))}'
            return f"{cmd} | exited with status={err.code}"
        else:
            return super().repr_failure(excinfo)

    def teardown(self):
        super().teardown()
        os.chdir(self.save_cwd)


class LocalRepo(pytest.File):
    def collect(self):
        args = ["--appendix", 'RUN echo "appendix" > /tmp/appendix']
        # If there's an extra-args.yaml file in a test dir, assume it contains
        # a yaml list with extra arguments to be passed to repo2docker
        extra_args_path = self.path.parent / "test-extra-args.yaml"
        if extra_args_path.exists():
            extra_args = yaml.safe_load(extra_args_path.read_text())
            args += extra_args

        print(self.path.name, self.path.parent, str(self.path))
        # re-use image name for multiple tests of the same image
        # so we don't run through the build twice
        rel_repo_dir = os.path.relpath(self.path.parent, TESTS_DIR)
        image_name = f"r2d-tests-{escapism.escape(rel_repo_dir, escape_char='-').lower()}-{int(time.time())}"
        args.append(f"--image-name={image_name}")
        args.append(str(self.path.parent))
        yield Repo2DockerTest.from_parent(self, name="build", args=args)

        yield Repo2DockerTest.from_parent(
            self,
            name=self.path.name,
            args=args + ["./verify"],
            skip_build=True,
        )

        # mount the tests dir as a volume
        check_tmp_args = (
            args[:-1]
            + ["--volume", f"{TESTS_DIR}:/io/tests"]
            + [args[-1], "/io/tests/check-tmp"]
        )

        yield Repo2DockerTest.from_parent(
            self,
            name="check-tmp",
            args=check_tmp_args,
            skip_build=True,
            extra_run_kwargs={"user": "root"},
        )


class RemoteRepoList(pytest.File):
    def collect(self):
        with self.path.open() as f:
            repos = yaml.safe_load(f)
        for repo in repos:
            args = []
            if "ref" in repo:
                args += ["--ref", repo["ref"]]
            args += [repo["url"], "--"] + shlex.split(repo["verify"])

            yield Repo2DockerTest.from_parent(self, name=repo["name"], args=args)
