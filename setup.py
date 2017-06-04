from __future__ import print_function

import hashlib
import os
import sys
import tarfile

try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from setuptools import setup, find_packages

tgz = 'source-to-image-v1.1.6-f519129-{}-amd64.tar.gz'.format(sys.platform)
s2i_bin_url = 'https://github.com/openshift/source-to-image/releases/download/v1.1.6/' + tgz

checksums = {
    'darwin': '0398bb5cd1d77a59ed9780ec4e2edd3b0c70e973d66b6ae5c072a8830029d703',
    'linux': '85ed735d141da1fe3def7826910c0c0baf587df6c727529b52d2c5cd98dcb641',
}


def download_s2i():
    if os.path.exists(tgz):
        print("Already have %s" % tgz)
        return
    print("Downloading %s" % s2i_bin_url)
    reader = urlopen(s2i_bin_url)
    with open(tgz, 'wb') as f:
        f.write(reader.read())
    reader.close()


def stage_s2i():
    """Stage s2i binary into repo2docker"""
    print("Staging %s" % s2i_dest)
    with tarfile.open(tgz) as f:
        f.extract('./s2i', pkg)


def checksum_s2i():
    """Check the checksum of the s2i binary"""
    with open(s2i_dest, 'rb') as f:
        found_hash = hashlib.sha256(f.read()).hexdigest()
    expected = checksums[sys.platform]
    if found_hash != expected:
        print("Checksum mismatch %s != %s" % (found_hash, expected))
    return found_hash == expected


def have_s2i():
    """Do we already have s2i?"""
    if not os.path.exists(s2i_dest):
        return False
    return checksum_s2i()


here = os.path.dirname(os.path.abspath(__file__))
pkg = os.path.join(here, 'repo2docker')

s2i_dest = os.path.join(pkg, 's2i')

if sys.platform in checksums:
    if not have_s2i():
        download_s2i()
        stage_s2i()

    if not checksum_s2i():
        print("s2i checksum failed", file=sys.stderr)
        sys.exit(1)
else:
    print("I don't know how to bundle s2i for %s" % sys.platform)

cmdclass = {}
try:
    from wheel.bdist_wheel import bdist_wheel
    from wheel.pep425tags import get_platform
except ImportError:
    # no wheel
    pass
else:
    # apply current platform tag
    # because we bundle platform-specific s2i binaries
    class PlatformBDistWheel(bdist_wheel):
        def initialize_options(self):
            super(PlatformBDistWheel, self).initialize_options()
            if self.plat_name is None:
                self.plat_name = get_platform()

    cmdclass['bdist_wheel'] = PlatformBDistWheel

setup(
    name='jupyter-repo2docker',
    version='0.2.6',
    install_requires=[
        'docker',
        'traitlets',
        'python-json-logger',
        'escapism'
    ],
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='BSD',
    cmdclass=cmdclass,
    package_data={
        'repo2docker': ['s2i'],
    },
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jupyter-repo2docker = repo2docker.__main__:main'
        ]
    },
)
