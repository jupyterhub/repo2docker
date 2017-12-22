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
    Test to check if repo2docker throws image_name validation error on --image-name argument containing uppercase characters.
    """

    builddir = os.path.dirname(__file__)

    assert not does_validate_image_name(builddir, 'Test/Invalid_name:1.0.0')

