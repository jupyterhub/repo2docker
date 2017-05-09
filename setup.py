from setuptools import setup, find_packages

setup(
    name='builder',
    version='0.1',
    install_requires=[
        'docker',
        'traitlets'
    ],
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='BSD',
    packages=find_packages(),
)
