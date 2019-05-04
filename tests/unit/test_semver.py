from repo2docker.buildpacks.julia import semver


def test_str_to_version():
    assert semver.str_to_version("1.5.2") == (1, 5, 2)
    assert semver.str_to_version("1") == (1,)


def test_major_minor_patch():
    V = (1, 2, 3)
    assert (semver.major(V), semver.minor(V), semver.patch(V)) == (1, 2, 3)
    assert semver.major((1,)) == 1
    assert semver.minor((1,)) == 0
    assert semver.patch((1,)) == 0


def test_simple_matches():
    assert repr(semver.create_semver_matcher("1.2.5")) == "[1.2.5-2)"
    assert repr(semver.create_semver_matcher("1.2.5")) == "[1.2.5-2)"
    assert repr(semver.create_semver_matcher("^1.2.3")) == "[1.2.3-2)"
    assert repr(semver.create_semver_matcher("^1.2")) == "[1.2-2)"
    assert repr(semver.create_semver_matcher("^1")) == "[1-2)"
    assert repr(semver.create_semver_matcher("^0.2.3")) == "[0.2.3-0.3)"
    assert repr(semver.create_semver_matcher("^0.0.3")) == "[0.0.3-0.0.4)"
    assert repr(semver.create_semver_matcher("^0.0")) == "[0.0-0.1)"
    assert repr(semver.create_semver_matcher("^0")) == "[0-1)"
    # This one seems wrong: `~1.2.3 = [1.2.3, 1.2.4)` but ~ is special in Julia
    # from https://docs.julialang.org/en/latest/stdlib/Pkg/#Tilde-specifiers-1
    assert repr(semver.create_semver_matcher("~1.2.3")) == "[1.2.3-1.2.4]"
    assert repr(semver.create_semver_matcher("~1.3.5")) == "[1.3.5-1.3.6]"
    assert repr(semver.create_semver_matcher("~1.2")) == "[1.2-1.3]"
    assert repr(semver.create_semver_matcher("~1")) == "[1-2]"


def test_range_matches():
    assert semver.create_semver_matcher(
        "1.2.3"
    ) == semver.create_semver_matcher("^1.2.3")
    assert semver.create_semver_matcher(
        "1.2.3"
    ) == semver.create_semver_matcher("^1.2.3")
    assert semver.create_semver_matcher("1.2") == semver.create_semver_matcher(
        "^1.2"
    )
    assert semver.create_semver_matcher("1") == semver.create_semver_matcher(
        "^1"
    )
    assert semver.create_semver_matcher(
        "0.0.3"
    ) == semver.create_semver_matcher("^0.0.3")
    assert semver.create_semver_matcher("0") == semver.create_semver_matcher(
        "^0"
    )


def test_match_particular_version():
    assert semver.create_semver_matcher("1.2.3").match(
        semver.str_to_version("1.5.2")
    )
    assert semver.create_semver_matcher("1.2.3").match(
        semver.str_to_version("1.2.3")
    )
    assert (
        semver.create_semver_matcher("1.2.3").match(
            semver.str_to_version("2.0.0")
        )
        == False
    )
    assert (
        semver.create_semver_matcher("1.2.3").match(
            semver.str_to_version("1.2.2")
        )
        == False
    )
    assert semver.create_semver_matcher("~1.2.3").match(
        semver.str_to_version("1.2.4")
    )
    assert semver.create_semver_matcher("~1.2.3").match(
        semver.str_to_version("1.2.3")
    )
    assert (
        semver.create_semver_matcher("~1.2.3").match(
            semver.str_to_version("1.3")
        )
        == False
    )
    assert semver.create_semver_matcher("1.2").match(
        semver.str_to_version("1.2.0")
    )
    assert semver.create_semver_matcher("1.2").match(
        semver.str_to_version("1.9.9")
    )
    assert (
        semver.create_semver_matcher("1.2").match(
            semver.str_to_version("2.0.0")
        )
        == False
    )
    assert (
        semver.create_semver_matcher("1.2").match(
            semver.str_to_version("1.1.9")
        )
        == False
    )
    assert semver.create_semver_matcher("0.2.3").match(
        semver.str_to_version("0.2.3")
    )
    assert (
        semver.create_semver_matcher("0.2.3").match(
            semver.str_to_version("0.3.0")
        )
        == False
    )
    assert (
        semver.create_semver_matcher("0.2.3").match(
            semver.str_to_version("0.2.2")
        )
        == False
    )
    assert semver.create_semver_matcher("0").match(
        semver.str_to_version("0.0.0")
    )
    assert semver.create_semver_matcher("0").match(
        semver.str_to_version("0.99.0")
    )
    assert (
        semver.create_semver_matcher("0").match(semver.str_to_version("1.0.0"))
        == False
    )
    assert semver.create_semver_matcher("0.0").match(
        semver.str_to_version("0.0.0")
    )
    assert semver.create_semver_matcher("0.0").match(
        semver.str_to_version("0.0.99")
    )
    assert (
        semver.create_semver_matcher("0.0").match(
            semver.str_to_version("0.1.0")
        )
        == False
    )


def test_less_than_prefix():
    assert repr(semver.create_semver_matcher("<1.2.3")) == "<1.2.3"
    assert repr(semver.create_semver_matcher("<1")) == "<1.0.0"
    assert repr(semver.create_semver_matcher("<0.2.3")) == "<0.2.3"

    assert semver.create_semver_matcher("<2.0.3").match(
        semver.str_to_version("2.0.2")
    )
    assert semver.create_semver_matcher("<2").match(
        semver.str_to_version("0.0.1")
    )
    assert semver.create_semver_matcher("<2.0.3").match(
        semver.str_to_version("0.2.3")
    )
    assert (
        semver.create_semver_matcher("<0.2.4").match(
            semver.str_to_version("0.2.4")
        )
        == False
    )


def test_equal_prefix():
    assert repr(semver.create_semver_matcher("=1.2.3")) == "==1.2.3"
    assert repr(semver.create_semver_matcher("=1.2")) == "==1.2.0"
    assert repr(semver.create_semver_matcher("  =1")) == "==1.0.0"
    assert semver.create_semver_matcher("=1.2.3").match(
        semver.str_to_version("1.2.3")
    )
    assert (
        semver.create_semver_matcher("=1.2.3").match(
            semver.str_to_version("1.2.4")
        )
        == False
    )
    assert (
        semver.create_semver_matcher("=1.2.3").match(
            semver.str_to_version("1.2.2")
        )
        == False
    )


def test_fancy_unicode():
    assert semver.create_semver_matcher(
        "≥1.3.0"
    ) == semver.create_semver_matcher(">=1.3.0")


def test_largerthan_equal():
    assert repr(semver.create_semver_matcher(">=   1.2.3")) == ">=   1.2.3"
    assert repr(semver.create_semver_matcher("  >=  1")) == ">=  1.0.0"
    assert semver.create_semver_matcher(">=1").match(
        semver.str_to_version("1.0.0")
    )
    assert semver.create_semver_matcher(">=0").match(
        semver.str_to_version("0.0.1")
    )
    assert semver.create_semver_matcher(">=1.2.3").match(
        semver.str_to_version("1.2.3")
    )
    assert (
        semver.create_semver_matcher(">=1.2.3").match(
            semver.str_to_version("1.2.2")
        )
        == False
    )
