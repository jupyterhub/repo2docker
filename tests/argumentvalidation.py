"""
Tests that runs validity checks on arguments passed in from shell
"""

import os
import subprocess


def validate_arguments(builddir, args_list, expected, disable_dockerd=False):
    """Helper to validate arguments passed in from the shell"""
    try:
        cmd = ['repo2docker']
        for k in args_list:
            cmd.append(k)
        cmd.append(builddir)

        env = os.environ.copy()
        if disable_dockerd:
            env['DOCKER_HOST'] = "INCORRECT"

        subprocess.check_output(cmd, env=env, stderr=subprocess.STDOUT)
        return True

    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        if expected in output:
            return False

        else:
            raise


def test_image_name_fail():
    """
    Check if validation error on --image-name argument containing uppercase
    characters and _ characters in incorrect positions.
    """
    image_name = 'Test/Invalid_name:1.0.0'

    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = (
        "%r is not a valid docker image name. Image name"
        "must start with an alphanumeric character and"
        "can then use _ . or - in addition to alphanumeric." % image_name
    )
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_underscore_fail():
    """
    Check if validation error on --image-name argument starts with _.
    """
    image_name = '_test/invalid_name:1.0.0'

    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = (
        "%r is not a valid docker image name. Image name"
        "must start with an alphanumeric character and"
        "can then use _ . or - in addition to alphanumeric." % image_name
    )
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_double_dot_fail():
    """
    Check if validation error on --image-name argument containing consecutive dots.
    """
    image_name = 'test..com/invalid_name:1.0.0'

    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = (
        "%r is not a valid docker image name. Image name"
        "must start with an alphanumeric character and"
        "can then use _ . or - in addition to alphanumeric." % image_name
    )
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_valid_restricted_registry_domain_name_fail():
    """
    Check validation error on --image-name argument being invalid based on the
    regex definitions first part of registry domain cannot contain uppercase
    characters
    """
    image_name = 'Test.com/valid_name:1.0.0'

    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = (
        "%r is not a valid docker image name. Image name"
        "must start with an alphanumeric character and"
        "can then use _ . or - in addition to alphanumeric." % image_name
    )
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_valid_registry_domain_name_success():
    """
    Check a valid --image-name argument with non-leading uppercase in domain
    name.
    """
    image_name = 'test.COM/valid_name:1.0.0'

    builddir = os.path.dirname(__file__) + '/dockerfile/simple/'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    assert validate_arguments(builddir, args_list, None)


def test_image_name_valid_name_success():
    """
    Check valid --image-name argument.
    """
    image_name = 'test.com/valid_name:1.0.0'

    builddir = os.path.dirname(__file__) + '/dockerfile/simple/'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    assert validate_arguments(builddir, args_list, None)


def test_volume_no_build_fail():
    """
    Check if repo2docker fails when both --no-build and -v arguments are given
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-build', '-v', '/data:/data']
    assert not validate_arguments(
        builddir,
        args_list,
        'To Mount volumes with -v, you also need to run the container',
    )


def test_volume_no_run_fail():
    """Check if repo2docker fails when both --no-run and -v arguments are given
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '-v', '/data:/data']
    assert not validate_arguments(
        builddir,
        args_list,
        'To Mount volumes with -v, you also need to run the container',
    )


def test_env_no_run_fail():
    """
    Check if repo2docker fails when both --no-run and -e arguments are given
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '-e', 'FOO=bar', '--']
    assert not validate_arguments(
        builddir,
        args_list,
        'To specify environment variables, you also need to run the container',
    )


def test_port_mapping_no_run_fail():
    """
    Check if repo2docker fails when passed --no-run and --publish arguments.
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '--publish', '8000:8000']
    assert not validate_arguments(
        builddir,
        args_list,
        'To publish user defined port mappings, the container must also be run',
    )


def test_all_ports_mapping_no_run_fail():
    """
    Check if repo2docker fails when passed both --no-run and -P arguments.
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '-P']
    assert not validate_arguments(
        builddir,
        args_list,
        'To publish user defined port mappings, the container must also be run',
    )


def test_invalid_port_mapping_fail():
    """
    Check if r2d fails when an invalid port is specified in the port mapping
    """
    builddir = os.path.dirname(__file__)
    # Specifying builddir here itself to simulate passing in a run command
    # builddir passed in the function will be an argument for the run command
    args_list = ['-p', '75000:80', builddir, 'ls']
    assert not validate_arguments(builddir, args_list, 'Invalid port mapping')


def test_invalid_protocol_port_mapping_fail():
    """
    Check if r2d fails when passed an invalid protocol (`tpc` instead of `tcp`)
    in the port mapping
    """
    builddir = os.path.dirname(__file__)
    # Specifying builddir here itself to simulate passing in a run command
    # builddir passed in the function will be an argument for the run command
    args_list = ['-p', '80/tpc:8000', builddir, 'ls']
    assert not validate_arguments(builddir, args_list, 'Invalid port mapping')


def test_invalid_container_port_protocol_mapping_fail():
    """
    Check if r2d fails when an invalid protocol is specified in the container
    port in port mapping
    """
    builddir = os.path.dirname(__file__)
    # Specifying builddir here itself to simulate passing in a run command
    # builddir passed in the function will be an argument for the run command
    args_list = ['-p', '80:8000/upd', builddir, 'ls']
    assert not validate_arguments(builddir, args_list, 'Invalid port mapping')


def test_docker_handle_fail():
    """
    Check if r2d fails with minimal error message when unable to connect to
    docker daemon. Setting `disable_dockerd=True` simulates an unavailable
    docker daemon.
    """
    args_list = []
    builddir = os.path.dirname(__file__) + '/../'
    assert not validate_arguments(
        builddir,
        args_list,
        "Docker client initialization error. Check if docker is running on the host.",
        True,
    )


def test_docker_handle_debug_fail():
    """
    Check if r2d fails with stack trace on when unable to connect to docker
    daemon and debug argument is passed. Setting `disable_dockerd=True`
    simulates an unavailable docker daemon.
    """
    args_list = ['--debug']
    builddir = os.path.dirname(__file__) + '/../'
    assert not validate_arguments(
        builddir, args_list, "docker.errors.DockerException", True
    )


def test_docker_no_build_success():
    """
    Check if r2d succeeds with --no-build argument when unable to connect to
    docker daemon as the daemon is not needed when not building an image.
    Setting `disable_dockerd=True` simulates an unavailable docker daemon.
    """
    args_list = ['--no-build', '--no-run']
    builddir = os.path.dirname(__file__) + '/../'
    assert validate_arguments(builddir, args_list, "", True)
