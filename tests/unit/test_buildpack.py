import re
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


# A Dockerfile double-quoted word: any char except a quote or a backslash, or
# a backslash followed by anything.
_LABEL_LINE = re.compile(r'^LABEL ("(?:[^"\\]|\\.)*")=("(?:[^"\\]|\\.)*")$')


def _unquote_dockerfile_word(word):
    """Decode a double-quoted Dockerfile word the way the builder does.

    Mirrors ``processDoubleQuote`` in BuildKit's ``frontend/dockerfile/shell``
    (and its identical ancestor in the Docker 17.09 classic builder): only
    ``\\``, ``"`` and ``$`` can be escaped, every other backslash is literal.
    """
    assert word.startswith('"') and word.endswith('"'), word
    body = word[1:-1]
    out = []
    i = 0
    while i < len(body):
        if body[i] == "\\" and i + 1 < len(body) and body[i + 1] in '"$\\':
            out.append(body[i + 1])
            i += 2
        else:
            out.append(body[i])
            i += 1
    return "".join(out)


@pytest.mark.parametrize(
    "label_value, expected",
    [
        # Injection attempts: a newline is not representable in a Dockerfile
        # word, so it is flattened rather than allowed to start a directive.
        ("hello\nRUN echo pwned", "hello\\nRUN echo pwned"),
        (
            "semicolon; pipe | newline\nstill same value",
            "semicolon; pipe | newline\\nstill same value",
        ),
        ('" ; RUN echo pwned ; LABEL x="', '" ; RUN echo pwned ; LABEL x="'),
        # Values that must survive byte for byte.
        ('value with "double" quotes', None),
        ("backtick `$(id)` and $VAR", None),
        (r"windows\path\to\file", None),
        ("trailing backslash\\", None),
        ("", None),
        ("héllo 中文 🎉", None),
    ],
)
def test_labels_with_special_chars_do_not_break_dockerfile(
    tmpdir, label_value, expected, base_image
):
    """Label values must land as exactly one token, decoding back unchanged.

    The template used to render ``LABEL k="{{v}}"`` with no escaping at all, so
    a value containing a literal newline followed by ``RUN ...`` became a real
    Dockerfile RUN directive at build time.

    ``expected`` is the value after decoding; ``None`` means it must round-trip
    unchanged. Newlines cannot be represented and are flattened to a literal
    backslash-n, which is the one lossy case.
    """
    if expected is None:
        expected = label_value

    tmpdir.chdir()
    bp = BaseImage(base_image)
    bp.labels = {"my.label": label_value}
    dockerfile = bp.render()

    label_lines = [
        line for line in dockerfile.splitlines() if line.startswith("LABEL ")
    ]
    assert len(label_lines) == 1, (
        f"expected exactly one LABEL line, found {len(label_lines)}: "
        f"{label_lines!r}"
    )

    # The value must not have broken out and started a directive of its own.
    assert not [
        line
        for line in dockerfile.splitlines()
        if line.startswith("RUN ") and "pwned" in line
    ], f"label value injected a top-level RUN:\n{dockerfile}"

    match = _LABEL_LINE.match(label_lines[0])
    assert match, f"LABEL line is not two quoted words: {label_lines[0]!r}"
    key, value = match.groups()

    # An unescaped $ would be substituted from the build environment.
    assert "$" not in re.sub(r"\\.", "", value), f"unescaped $ in {value!r}"

    assert _unquote_dockerfile_word(key) == "my.label"
    assert _unquote_dockerfile_word(value) == expected
