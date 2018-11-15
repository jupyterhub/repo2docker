from setuptools import setup, find_packages
import sys
import versioneer

if sys.version_info[0] < 3:
    readme = None
else:
    with open('README.md', encoding="utf8") as f:
        readme = f.read()

setup(
    name='jupyter-repo2docker',
    version=versioneer.get_version(),
    install_requires=[
        'docker',
        'traitlets',
        'python-json-logger',
        'escapism',
        'jinja2',
        'ruamel.yaml>=0.15',
    ],
    python_requires='>=3.4',
    author='Project Jupyter Contributors',
    author_email='jupyter@googlegroups.com',
    url='https://repo2docker.readthedocs.io/en/latest/',
    project_urls = {
        'Documentation': 'https://repo2docker.readthedocs.io',
        'Funding': 'https://jupyter.org/about',
        'Source': 'https://github.com/jupyter/repo2docker/',
        'Tracker': 'https://github.com/jupyter/repo2docker/issues',
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="reproducible science environments docker",
    description = "Repo2docker: Turn code repositories into Jupyter enabled Docker Images",
    long_description = readme,
    long_description_content_type = 'text/markdown',
    license='BSD',
    classifiers = [
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
    packages=find_packages(),
    include_package_data=True,
    cmdclass=versioneer.get_cmdclass(),
    entry_points={
        'console_scripts': [
            'jupyter-repo2docker = repo2docker.__main__:main',
            'repo2docker = repo2docker.__main__:main',
        ]
    },
)
