import pytest
from semver import VersionInfo

from repo2docker import semver


@pytest.mark.parametrize("test_input, expected", [("1.5.2", (1, 5, 2)), ("1", (1,))])
def test_str_to_version(test_input, expected):
    assert semver.str_to_version(test_input) == expected


def test_major_minor_patch():
    V = (1, 2, 3)
    assert (semver.major(V), semver.minor(V), semver.patch(V)) == (1, 2, 3)
    assert semver.major((1,)) == 1
    assert semver.minor((1,)) == 0
    assert semver.patch((1,)) == 0


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1.2.5", "[1.2.5-2)"),
        ("1.2.5", "[1.2.5-2)"),
        ("^1.2.3", "[1.2.3-2)"),
        ("^1.2", "[1.2-2)"),
        ("^1", "[1-2)"),
        ("^0.2.3", "[0.2.3-0.3)"),
        ("^0.0.3", "[0.0.3-0.0.4)"),
        ("^0.0", "[0.0-0.1)"),
        ("^0", "[0-1)"),
        # https://pkgdocs.julialang.org/v1/compatibility/#Tilde-specifiers
        ("~1.2.3", "[1.2.3-1.3)"),
        ("~1.3.5", "[1.3.5-1.4)"),
        ("~1.2", "[1.2-1.3)"),
        ("~1", "[1-2)"),
        ("~0.0.3", "[0.0.3-0.0.4)"),
        ("~0.0", "[0.0-0.1)"),
        ("~0", "[0-1)"),
    ],
)
def test_simple_matches(test_input, expected):
    assert repr(semver.create_semver_matcher(test_input)) == expected


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1.2.3", "^1.2.3"),
        ("1.2", "^1.2"),
        ("1", "^1"),
        ("0.0.3", "^0.0.3"),
        ("0", "^0"),
    ],
)
def test_range_matches(test_input, expected):
    assert semver.create_semver_matcher(test_input) == semver.create_semver_matcher(
        expected
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1.2.3", "1.5.2"),
        ("1.2.3", "1.2.3"),
        ("~1.2.3", "1.2.4"),
        ("~1.2.3", "1.2.3"),
        ("~1.2", "1.2.10"),
        ("~1", "1.99"),
        ("~0.0.3", "0.0.3"),
        ("1.2", "1.2.0"),
        ("1.2", "1.9.9"),
        ("0.2.3", "0.2.3"),
        ("0", "0.0.0"),
        ("0", "0.99.0"),
        ("0.0", "0.0.0"),
        ("0.0", "0.0.99"),
    ],
)
def test_match_particular_version_expected_true(test_input, expected):
    assert semver.create_semver_matcher(test_input).match(
        semver.str_to_version(expected)
    )


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("1.2.3", "2.0.0"),
        ("1.2.3", "1.2.2"),
        ("~1.2.3", "1.3"),
        ("~1.2", "1.3"),
        ("~1", "2"),
        ("~0.0.3", "0.0.4"),
        ("1.2", "2.0.0"),
        ("1.2", "1.1.9"),
        ("0.2.3", "0.3.0"),
        ("0.2.3", "0.2.2"),
        ("0", "1.0.0"),
        ("0.0", "0.1.0"),
    ],
)
def test_match_particular_version_expected_false(test_input, expected):
    assert (
        semver.create_semver_matcher(test_input).match(semver.str_to_version(expected))
        == False
    )


def test_less_than_prefix():
    assert repr(semver.create_semver_matcher("<1.2.3")) == "<1.2.3"
    assert repr(semver.create_semver_matcher("<1")) == "<1.0.0"
    assert repr(semver.create_semver_matcher("<0.2.3")) == "<0.2.3"

    assert semver.create_semver_matcher("<2.0.3").match(semver.str_to_version("2.0.2"))
    assert semver.create_semver_matcher("<2").match(semver.str_to_version("0.0.1"))
    assert semver.create_semver_matcher("<2.0.3").match(semver.str_to_version("0.2.3"))
    assert (
        semver.create_semver_matcher("<0.2.4").match(semver.str_to_version("0.2.4"))
        == False
    )


@pytest.mark.parametrize("test_input, expected", [("≥1.3.0", ">=1.3.0")])
def test_fancy_unicode(test_input, expected):
    assert semver.create_semver_matcher(test_input) == semver.create_semver_matcher(
        expected
    )


def test_equal_prefix():
    assert repr(semver.create_semver_matcher("=1.2.3")) == "==1.2.3"
    assert repr(semver.create_semver_matcher("=1.2")) == "==1.2.0"
    assert repr(semver.create_semver_matcher("  =1")) == "==1.0.0"
    assert semver.create_semver_matcher("=1.2.3").match(semver.str_to_version("1.2.3"))
    assert (
        semver.create_semver_matcher("=1.2.3").match(semver.str_to_version("1.2.4"))
        == False
    )
    assert (
        semver.create_semver_matcher("=1.2.3").match(semver.str_to_version("1.2.2"))
        == False
    )


def test_largerthan_equal():
    assert repr(semver.create_semver_matcher(">=   1.2.3")) == ">=   1.2.3"
    assert repr(semver.create_semver_matcher("  >=  1")) == ">=  1.0.0"
    assert semver.create_semver_matcher(">=1").match(semver.str_to_version("1.0.0"))
    assert semver.create_semver_matcher(">=0").match(semver.str_to_version("0.0.1"))
    assert semver.create_semver_matcher(">=1.2.3").match(semver.str_to_version("1.2.3"))
    assert (
        semver.create_semver_matcher(">=1.2.3").match(semver.str_to_version("1.2.2"))
        == False
    )


@pytest.mark.parametrize(
    "vstr, expected",
    [
        ("1.2.3", "1.2.3"),
        ("1.2", "1.2.0"),
        ("1", "1.0.0"),
    ],
)
def test_parse_version(vstr, expected):
    version_info = semver.parse_version(vstr)
    assert isinstance(version_info, semver.semver.VersionInfo)
    assert str(version_info) == expected
    # satisfies itself, since this is how we use it
    assert semver.parse_version(expected) <= version_info
    assert semver.parse_version(expected) >= version_info
