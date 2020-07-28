"""
Tests that runs validity checks on arguments passed in from shell
"""

import os
import subprocess

import pytest


here = os.path.dirname(os.path.abspath(__file__))
test_dir = os.path.dirname(here)
docker_simple = os.path.join(test_dir, "dockerfile", "simple")

# default to building in the cwd (a temporary directory)
builddir = "."


@pytest.fixture
def temp_cwd(tmpdir):
    tmpdir.chdir()


invalid_image_name_template = (
    "%r is not a valid docker image name. Image name "
    "must start with a lowercase or numeric character and "
    "can then use _ . or - in addition to lowercase and numeric."
)


def validate_arguments(builddir, args_list=".", expected=None, disable_dockerd=False):
    try:
        cmd = ["repo2docker"]
        for k in args_list:
            cmd.append(k)
        cmd.append(builddir)
        env = os.environ.copy()
        if disable_dockerd:
            env["DOCKER_HOST"] = "INCORRECT"
        subprocess.check_output(cmd, env=env, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        if expected is not None:
            assert expected in output
            return False
        else:
            print(output)
            raise


def test_image_name_fail(temp_cwd):
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument containing
    uppercase characters and _ characters in incorrect positions.
    """

    image_name = "Test/Invalid_name:1.0.0"
    args_list = ["--no-run", "--no-build", "--image-name", image_name]
    expected = invalid_image_name_template % image_name
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_underscore_fail(temp_cwd):
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument starts with _.
    """

    image_name = "_test/invalid_name:1.0.0"
    args_list = ["--no-run", "--no-build", "--image-name", image_name]
    expected = invalid_image_name_template % image_name
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_double_dot_fail(temp_cwd):
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument contains consecutive dots.
    """

    image_name = "test..com/invalid_name:1.0.0"
    args_list = ["--no-run", "--no-build", "--image-name", image_name]
    expected = invalid_image_name_template % image_name
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_valid_restircted_registry_domain_name_fail(temp_cwd):
    """
    Test to check if repo2docker throws image_name validation error on -image-name argument being invalid. Based on the
    regex definitions first part of registry domain cannot contain uppercase characters
    """

    image_name = "Test.com/valid_name:1.0.0"
    args_list = ["--no-run", "--no-build", "--image-name", image_name]
    expected = invalid_image_name_template % image_name
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_valid_registry_domain_name_success(temp_cwd):
    """
    Test to check if repo2docker runs with a valid --image-name argument.
    """

    builddir = docker_simple
    image_name = "test.COM/valid_name:1.0.0"
    args_list = ["--no-run", "--no-build", "--image-name", image_name]

    assert validate_arguments(builddir, args_list, None)


def test_image_name_valid_name_success(temp_cwd):
    """
    Test to check if repo2docker runs with a valid --image-name argument.
    """

    builddir = docker_simple
    image_name = "test.com/valid_name:1.0.0"
    args_list = ["--no-run", "--no-build", "--image-name", image_name]

    assert validate_arguments(builddir, args_list, None)


def test_volume_no_build_fail(temp_cwd):
    """
    Test to check if repo2docker fails when both --no-build and -v arguments are given
    """
    args_list = ["--no-build", "-v", "/data:/data"]

    assert not validate_arguments(
        builddir, args_list, "Cannot mount volumes if container is not run"
    )


def test_volume_no_run_fail(temp_cwd):
    """
    Test to check if repo2docker fails when both --no-run and -v arguments are given
    """
    args_list = ["--no-run", "-v", "/data:/data"]

    assert not validate_arguments(
        builddir, args_list, "Cannot mount volumes if container is not run"
    )


def test_env_no_run_fail(temp_cwd):
    """
    Test to check if repo2docker fails when both --no-run and -e arguments are given
    """
    args_list = ["--no-run", "-e", "FOO=bar", "--"]

    assert not validate_arguments(
        builddir,
        args_list,
        "To specify environment variables, you also need to run the container",
    )


def test_port_mapping_no_run_fail(temp_cwd):
    """
    Test to check if repo2docker fails when both --no-run and --publish arguments are specified.
    """
    args_list = ["--no-run", "--publish", "8000:8000"]

    assert not validate_arguments(
        builddir,
        args_list,
        "To publish user defined port mappings, the container must also be run",
    )


def test_all_ports_mapping_no_run_fail(temp_cwd):
    """
    Test to check if repo2docker fails when both --no-run and -P arguments are specified.
    """
    args_list = ["--no-run", "-P"]

    assert not validate_arguments(
        builddir,
        args_list,
        "To publish user defined port mappings, the container must also be run",
    )


def test_invalid_port_mapping_fail(temp_cwd):
    """
    Test to check if r2d fails when an invalid port is specified in the port mapping
    """
    # Specifying builddir here itself to simulate passing in a run command
    # builddir passed in the function will be an argument for the run command
    args_list = ["-p", "75000:80", builddir, "ls"]

    assert not validate_arguments(builddir, args_list, "Port specification")


def test_invalid_protocol_port_mapping_fail(temp_cwd):
    """
    Test to check if r2d fails when an invalid protocol is specified in the port mapping
    """
    # Specifying builddir here itself to simulate passing in a run command
    # builddir passed in the function will be an argument for the run command
    args_list = ["-p", "80/tpc:8000", builddir, "ls"]

    assert not validate_arguments(builddir, args_list, "Port specification")


def test_invalid_container_port_protocol_mapping_fail(temp_cwd):
    """
    Test to check if r2d fails when an invalid protocol is specified in the container port in port mapping
    """
    # Specifying builddir here itself to simulate passing in a run command
    # builddir passed in the function will be an argument for the run command
    args_list = ["-p", "80:8000/upd", builddir, "ls"]

    assert not validate_arguments(builddir, args_list, "Port specification")


def test_docker_handle_fail(temp_cwd):
    """
    Test to check if r2d fails with minimal error message on not being able to connect to docker daemon
    """
    args_list = []

    assert not validate_arguments(
        builddir,
        args_list,
        "Check if docker is running on the host.",
        disable_dockerd=True,
    )


def test_docker_handle_debug_fail(temp_cwd):
    """
    Test to check if r2d fails with helpful error message on not being able to connect to docker daemon and debug enabled
    """
    args_list = ["--debug"]

    assert not validate_arguments(
        builddir,
        args_list,
        "Check if docker is running on the host.",
        disable_dockerd=True,
    )


def test_docker_no_build_success(temp_cwd):
    """
    Test to check if r2d succeeds with --no-build argument with not being able to connect to docker daemon
    """
    args_list = ["--no-build", "--no-run"]

    assert validate_arguments(builddir, args_list, disable_dockerd=True)
