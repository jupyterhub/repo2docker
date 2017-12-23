"""
Tests that runs validity checks on arguments passed in from shell
"""

import os
import subprocess

def does_validate_image_name(builddir, image_name):
    try:
        output = subprocess.check_output(
            [
                'repo2docker',
                '--no-run',
                '--no-build',
                '--image-name',
                str(image_name),
                builddir
            ],
            stderr=subprocess.STDOUT,
        ).decode()
        return True
    except subprocess.CalledProcessError as e:
        output = e.output.decode()
        if "error: argument --image-name: %r is not a valid docker image name. " \
           "Image name can contain only lowercase characters." % image_name in output:
            return False
        else:
            raise


def test_image_name_fail():
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument containing
    uppercase characters and _ characters in incorrect positions.
    """

    builddir = os.path.dirname(__file__)

    assert not does_validate_image_name(builddir, 'Test/Invalid_name:1.0.0')


def test_image_name_underscore_fail():
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument starts with _.
    """

    builddir = os.path.dirname(__file__)

    assert not does_validate_image_name(builddir, '_test/invalid_name:1.0.0')


def test_image_name_double_dot_fail():
    """
    Test to check if repo2docker throws image_name validation error on --image-name argument contains consecutive dots.
    """

    builddir = os.path.dirname(__file__)

    assert not does_validate_image_name(builddir, 'test..com/invalid_name:1.0.0')


def test_image_name_valid_restircted_registry_domain_name_fail():
    """
    Test to check if repo2docker throws image_name validation error on -image-name argument being invalid. Based on the
    regex definitions first part of registry domain cannot contain uppercase characters
    """

    builddir = os.path.dirname(__file__)

    assert not does_validate_image_name(builddir, 'Test.com/valid_name:1.0.0')


def test_image_name_valid_registry_domain_name_success():
    """
    Test to check if repo2docker runs with a valid --image-name argument.
    """

    builddir = os.path.dirname(__file__) + '/dockerfile/simple/'

    assert does_validate_image_name(builddir, 'test.COM/valid_name:1.0.0')


def test_image_name_valid_name_success():
    """
    Test to check if repo2docker runs with a valid --image-name argument.
    """

    builddir = os.path.dirname(__file__) + '/dockerfile/simple/'

    assert does_validate_image_name(builddir, 'test.com/valid_name:1.0.0')