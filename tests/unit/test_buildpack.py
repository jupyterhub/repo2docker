import shlex
from datetime import date
from os.path import join as pjoin
from tempfile import TemporaryDirectory

import pytest

from repo2docker.buildpacks import (
    BaseImage,
    LegacyBinderDockerBuildPack,
    PythonBuildPack,
)
from repo2docker.utils import chdir


def test_legacy_raises(base_image):
    # check legacy buildpack raises on a repo that triggers it
    with TemporaryDirectory() as repodir:
        with open(pjoin(repodir, "Dockerfile"), "w") as d:
            d.write("FROM andrewosh/binder-base")

        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack(base_image)
            with pytest.raises(RuntimeError):
                bp.detect()


def test_legacy_doesnt_detect(base_image):
    # check legacy buildpack doesn't trigger
    with TemporaryDirectory() as repodir:
        with open(pjoin(repodir, "Dockerfile"), "w") as d:
            d.write("FROM andrewosh/some-image")

        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack(base_image)
            assert not bp.detect()


def test_legacy_on_repo_without_dockerfile(base_image):
    # check legacy buildpack doesn't trigger on a repo w/o Dockerfile
    with TemporaryDirectory() as repodir:
        with chdir(repodir):
            bp = LegacyBinderDockerBuildPack(base_image)
            assert not bp.detect()


@pytest.mark.parametrize("python_version", ["2.6", "3.0", "4.10", "3.99"])
def test_unsupported_python(tmpdir, python_version, base_image):
    tmpdir.chdir()
    bp = PythonBuildPack(base_image)
    bp._python_version = python_version
    assert bp.python_version == python_version
    with pytest.raises(ValueError):
        bp.render()


@pytest.mark.parametrize(
    "runtime_txt, expected",
    [
        (None, (None, None, None)),
        ("abc-001", ("abc", "001", None)),
        ("abc-001-2025-06-22", ("abc", "001", date(2025, 6, 22))),
        ("abc-2025-06-22", ("abc", None, date(2025, 6, 22))),
        ("a_b/c-0.0.1-2025-06-22", ("a_b/c", "0.0.1", date(2025, 6, 22))),
    ],
)
def test_runtime(tmpdir, runtime_txt, expected, base_image):
    tmpdir.chdir()

    if runtime_txt is not None:
        with open("runtime.txt", "w") as f:
            f.write(runtime_txt)

    base = BaseImage(base_image)
    assert base.runtime == expected


@pytest.mark.parametrize(
    "runtime_txt",
    [
        "",
        "abc",
        "abc-001-25-06-22",
    ],
)
def test_invalid_runtime(tmpdir, runtime_txt, base_image):
    tmpdir.chdir()

    if runtime_txt is not None:
        with open("runtime.txt", "w") as f:
            f.write(runtime_txt)

    base = BaseImage(base_image)

    with pytest.raises(ValueError, match=r"^Invalid runtime.txt.*"):
        base.runtime


@pytest.mark.parametrize(
    "label_value, expected",
    [
        # A Dockerfile word cannot contain a newline, so newlines are
        # replaced with a literal backslash-n.
        ("hello\nRUN echo pwned", "hello\\nRUN echo pwned"),
        (
            'x"\nRUN echo pwned\nLABEL y="z',
            'x"\\nRUN echo pwned\\nLABEL y="z',
        ),
        ("carriage\rreturn", "carriage\\rreturn"),
        # Everything else must come back unchanged.
        ('" ; RUN echo pwned ; LABEL x="', None),
        ('value with "double" quotes', None),
        ("it's", None),
        ("backtick `$(id)` and $VAR", None),
        (r"windows\path\to\file", None),
        ("trailing backslash\\", None),
        ("", None),
        ("héllo 中文 🎉", None),
    ],
)
def test_labels_with_special_chars(tmpdir, label_value, expected, base_image):
    """A label must render as a single LABEL directive, whatever it contains.

    The template used to render ``LABEL k="{{v}}"`` without escaping the
    value, so one containing quotes or newlines could end the directive early
    and start new ones.

    ``expected`` is the value after unquoting; ``None`` means unchanged.
    Decoding uses ``shlex.split``, so this checks the rendering and not how a
    Dockerfile parser reads it.
    """
    if expected is None:
        expected = label_value

    tmpdir.chdir()
    bp = BaseImage(base_image)
    bp.labels = {"my label": label_value}
    dockerfile = bp.render()

    label_lines = [
        line for line in dockerfile.splitlines() if line.startswith("LABEL ")
    ]
    assert len(label_lines) == 1, label_lines
    assert shlex.split(label_lines[0]) == ["LABEL", f"my label={expected}"]
    assert "\nRUN echo pwned" not in dockerfile
