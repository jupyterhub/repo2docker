from setuptools import find_packages, setup

setup(
    name="Dummy",
    version="1.0.0",
    url="https://git-place.org/dummy/dummy.git",
    author="Dummy Name",
    author_email="dummy@my-email.com",
    description="Dummy package for testing purposes only",
    packages=find_packages(),
    install_requires=["pypi-pkg-test==0.0.4"],
)
