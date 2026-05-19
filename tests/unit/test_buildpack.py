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
    "label_value",
    [
        "hello\nRUN echo pwned",
        'value with "double" quotes',
        "backtick `$(id)` and $VAR",
        "semicolon; pipe | newline\nstill same value",
    ],
)
def test_labels_with_special_chars_do_not_break_dockerfile(
    tmpdir, label_value, base_image
):
    """Operator-supplied label values containing newlines, quotes, or shell
    metacharacters must not introduce extra Dockerfile directives.

    The previous template rendered ``LABEL k="{{v}}"`` with no escaping, so a
    value containing a literal newline followed by ``RUN ...`` produced a real
    Dockerfile RUN directive at build time. Apply ``shlex.quote`` to both key
    and value so that the value lands as a single quoted token regardless of
    its contents.
    """
    tmpdir.chdir()
    bp = BaseImage(base_image)
    bp.labels = {"my.label": label_value}
    dockerfile = bp.render()

    # Find the single LABEL directive that carries our key.
    label_lines = [
        line
        for line in dockerfile.splitlines()
        if line.startswith("LABEL ") and "my.label" in line
    ]
    assert len(label_lines) == 1, (
        f"expected exactly one LABEL line for my.label, found "
        f"{len(label_lines)}: {label_lines!r}"
    )

    # No subsequent top-level directive should appear that wasn't there
    # before. In particular, no `RUN echo pwned` injected as its own line.
    top_level_runs = [
        line
        for line in dockerfile.splitlines()
        if line.startswith("RUN ") and "pwned" in line
    ]
    assert not top_level_runs, (
        f"label value broke out of LABEL directive and produced an extra "
        f"top-level RUN: {top_level_runs!r}"
    )
