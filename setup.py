from distutils.cmd import Command
from setuptools import setup, find_packages
import sys
import versioneer

if sys.version_info[0] < 3:
    readme = None
else:
    with open("README.md", encoding="utf8") as f:
        readme = f.read()


class GenerateDataverseInstallationsFileCommand(Command):
    description = "Generate Dataverse installations data map"
    user_options = []

    def initialize_options(self):
        self.url = (
            "https://services.dataverse.harvard.edu/miniverse/map/installations-json"
        )

    def finalize_options(self):
        pass

    def run(self):
        from urllib.request import urlopen
        import json

        resp = urlopen(self.url, timeout=5)
        resp_body = resp.read()
        data = json.loads(resp_body.decode("utf-8"))
        if "installations" not in data:
            raise ValueError("Malformed installation map.")

        def get_identifier(json):
            return int(json["id"])

        data["installations"].sort(key=get_identifier)
        with open("repo2docker/contentproviders/dataverse.json", "w") as fp:
            json.dump(data, fp, indent=4, sort_keys=True)


__cmdclass = versioneer.get_cmdclass()
__cmdclass["generate_dataverse_file"] = GenerateDataverseInstallationsFileCommand

setup(
    name="jupyter-repo2docker",
    version=versioneer.get_version(),
    install_requires=[
        "docker",
        "traitlets",
        "python-json-logger",
        "escapism",
        "jinja2",
        "requests",
        "ruamel.yaml>=0.15",
        "toml",
        "semver",
    ],
    python_requires=">=3.6",
    author="Project Jupyter Contributors",
    author_email="jupyter@googlegroups.com",
    url="https://repo2docker.readthedocs.io/en/latest/",
    project_urls={
        "Documentation": "https://repo2docker.readthedocs.io",
        "Funding": "https://jupyter.org/about",
        "Source": "https://github.com/jupyterhub/repo2docker/",
        "Tracker": "https://github.com/jupyterhub/repo2docker/issues",
    },
    # this should be a whitespace separated string of keywords, not a list
    keywords="reproducible science environments docker",
    description="Repo2docker: Turn code repositories into Jupyter enabled Docker Images",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="BSD",
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    cmdclass=__cmdclass,
    entry_points={
        "console_scripts": [
            "jupyter-repo2docker = repo2docker.__main__:main",
            "repo2docker = repo2docker.__main__:main",
        ]
    },
)
