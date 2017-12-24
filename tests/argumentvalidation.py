"""
Tests that runs validity checks on arguments passed in from shell
"""

import os
import subprocess

def validate_arguments(builddir, args_list, expected):
    try:
        cmd = ['repo2docker']
        for k in args_list:
            cmd.append(k)
        cmd.append(builddir)
        subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        return True
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        if expected in output:
            return False
        else:
            raise


def test_image_name_fail():
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument containing
    uppercase characters and _ characters in incorrect positions.
    """

    builddir = os.path.dirname(__file__)
    image_name = 'Test/Invalid_name:1.0.0'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = "error: argument --image-name: %r is not a valid docker image name. " \
               "Image name can contain only lowercase characters." % image_name
    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_underscore_fail():
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument starts with _.
    """

    builddir = os.path.dirname(__file__)
    image_name = '_test/invalid_name:1.0.0'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = "error: argument --image-name: %r is not a valid docker image name. " \
               "Image name can contain only lowercase characters." % image_name

    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_double_dot_fail():
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument contains consecutive dots.
    """

    builddir = os.path.dirname(__file__)
    image_name = 'test..com/invalid_name:1.0.0'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = "error: argument --image-name: %r is not a valid docker image name. " \
               "Image name can contain only lowercase characters." % image_name

    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_valid_restircted_registry_domain_name_fail():
    """
    Test to check if repo2docker throws image_name validation error on -image-name argument being invalid. Based on the
    regex definitions first part of registry domain cannot contain uppercase characters
    """

    builddir = os.path.dirname(__file__)
    image_name = 'Test.com/valid_name:1.0.0'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]
    expected = "error: argument --image-name: %r is not a valid docker image name. " \
               "Image name can contain only lowercase characters." % image_name

    assert not validate_arguments(builddir, args_list, expected)


def test_image_name_valid_registry_domain_name_success():
    """
    Test to check if repo2docker runs with a valid --image-name argument.
    """

    builddir = os.path.dirname(__file__) + '/dockerfile/simple/'
    image_name = 'test.COM/valid_name:1.0.0'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]

    assert validate_arguments(builddir, args_list, None)


def test_image_name_valid_name_success():
    """
    Test to check if repo2docker runs with a valid --image-name argument.
    """

    builddir = os.path.dirname(__file__) + '/dockerfile/simple/'
    image_name = 'test.com/valid_name:1.0.0'
    args_list = ['--no-run', '--no-build', '--image-name', image_name]

    assert validate_arguments(builddir, args_list, None)

def test_volume_no_build_fail():
    """
    Test to check if repo2docker fails when both --no-build and -v arguments are given
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-build', '-v', '/data:/data']

    assert not validate_arguments(builddir, args_list, 'To Mount volumes with -v, you also need to run the container')


def test_volume_no_run_fail():
    """
    Test to check if repo2docker fails when both --no-run and -v arguments are given
    """
    builddir = os.path.dirname(__file__)
    args_list = ['--no-run', '-v', '/data:/data']

    assert not validate_arguments(builddir, args_list, 'To Mount volumes with -v, you also need to run the container')