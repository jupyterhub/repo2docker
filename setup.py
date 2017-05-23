from setuptools import setup, find_packages

setup(
    name='jupyter-repo2docker',
    version='0.1',
    install_requires=[
        'docker',
        'traitlets',
        'python-json-logger',
        'escapism'
    ],
    author='Yuvi Panda',
    author_email='yuvipanda@gmail.com',
    license='BSD',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'jupyter-repo2docker = repo2docker.__main__:main'
        ]
    },
)
