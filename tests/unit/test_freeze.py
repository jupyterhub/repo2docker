import os
from tempfile import TemporaryDirectory
from unittest.mock import patch

import pytest
from ruamel.yaml import YAML

from repo2docker.buildpacks.conda.freeze import set_python

V = "3.7"
yaml = YAML(typ="rt")


def test_set_python():
    with TemporaryDirectory() as d:
        env_fname = os.path.join(d, "some-env.yml")

        # function being tested
        set_python(env_fname, V)

        # check that set_python() did its job
        with open(env_fname) as f:
            env = yaml.load(f)
            f.seek(0)
            assert "AUTO GENERATED FROM" in f.readline()

        for dep in env["dependencies"]:
            # the "- pip:" entry isn't a string, hence this complex if
            # statement
            if isinstance(dep, str) and dep.startswith("python="):
                assert dep == f"python={V}.*", f"Unexpected dependency spec: '{dep}'"
                break
        else:
            assert False, f"Did not find 'python={V}.*' listed in the generated file"


def test_doesnt_clobber():
    # check a file not containing the word GENERATED on the first line is
    # left unchanged
    with TemporaryDirectory() as d:
        env_fname = os.path.join(d, "some-env.yml")
        with open(env_fname, "w") as f:
            f.write("some text here")

        set_python(env_fname, V)

        with open(env_fname) as f:
            assert f.read() == "some text here"


def test_python_missing_in_source_env():
    # check we raise an exception when python isn't in the source environemt
    with TemporaryDirectory() as d:
        # prep our source environment
        source_env_fname = os.path.join(d, "source-env.yml")
        with open(source_env_fname, "w") as f:
            yaml.dump({"dependencies": ["a_package_name=1.2.3"]}, f)

        with patch("repo2docker.buildpacks.conda.freeze.ENV_FILE", source_env_fname):
            target_env_fname = os.path.join(d, "some-env.yml")

            with pytest.raises(ValueError) as e:
                set_python(target_env_fname, V)

            assert "python dependency not found" in str(e.value)
