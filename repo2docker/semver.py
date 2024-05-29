"""
Julia specific handling of SemVer strings

It uses the python "semver" package to do most version string comparisons, but
the places where julia's SemVer handling differs from the semver package have
been implemented directly.

We use tuples to represent a Version, and functors as "matchers". The
matcher functors take a version string and return True if it passes its
constraints.
"""

import re
from functools import lru_cache

import semver


def find_semver_match(constraint, versions_list):
    """Find first version in a list of versions that matches a constraint"""
    matcher = create_semver_matcher(constraint)
    for vstr in reversed(versions_list):
        if matcher.match(str_to_version(vstr)):
            return vstr
    return None


def str_to_version(vstr):
    """Convert a simple x[.y[.z]] version string to a tuple of ints"""
    return tuple([int(n) for n in vstr.split(".")])


@lru_cache()
def parse_version(vstr):
    """Convert a simple 'x[.y[.z]]' version string to a comparable VersionInfo

    Wraps semver.VersionInfo.parse with zero-padding,
    so it can accept '1.0', where upstream only accepts exactly 3 version fields.
    """
    try:
        return semver.VersionInfo.parse(vstr)
    except ValueError:
        # may fail for e.g. short 1.0 versions
        n_fields = vstr.count(".")
        if n_fields < 2:
            vstr = vstr + (".0" * (2 - n_fields))
            return semver.VersionInfo.parse(vstr)
        else:
            raise


# Helpers
def major(v):
    return v[0]


def minor(v):
    return v[1] if len(v) >= 2 else 0


def patch(v):
    return v[2] if len(v) >= 3 else 0


@lru_cache()
def create_semver_matcher(constraint_str):
    """Create a matcher that can be used to match version tuples

    Version tuples are matched against the provided regex `constraint_str`.
    """
    constraint_str = constraint_str.strip()
    first_digit = re.search(r"\d", constraint_str)
    if not first_digit:
        # Invalid version string (no numbers in it)
        return ""
    constraint = str_to_version(constraint_str[first_digit.start() :])

    comparison_symbol = constraint_str[0 : first_digit.start()].strip()

    # Default to "^" search if no matching mode specified (up to next major version)
    if (first_digit.start() == 0) or (comparison_symbol == "^"):
        if major(constraint) == 0:
            # Also, julia treats pre-1.0 releases specially, as if the first
            # non-zero number is actually a major number:
            # https://docs.julialang.org/en/latest/stdlib/Pkg/#Caret-specifiers-1
            # So we need to handle it separately by bumping the first non-zero
            # enumber.
            for i, n in enumerate(constraint):
                if (
                    n != 0 or i == len(constraint) - 1
                ):  # (using the last existing number handles situations like "^0.0" or "^0")
                    upper = constraint[0:i] + (n + 1,)
                    break
            return VersionRange(constraint, upper, True)
        else:
            return VersionRange(constraint, (major(constraint) + 1,), True)

    # '~' matching, bumps minor version unless only major specified or leading 0.0.
    # https://pkgdocs.julialang.org/v1/compatibility/#Tilde-specifiers
    if comparison_symbol == "~":
        if len(constraint) == 1:
            # only major specified
            # ~x -> [x-x+1)
            return VersionRange(constraint, (constraint[0] + 1,), exclusive=True)
        elif len(constraint) == 2:
            # ~x.y -> [x.y-x.y+1)
            return VersionRange(
                constraint,
                (
                    major(constraint),
                    minor(constraint) + 1,
                ),
                exclusive=True,
            )
        else:
            # 3 parts, different depending on if starts with 0.0
            if major(constraint) == 0 and minor(constraint) == 0:
                # ~0.0.3 = [0.0.3-0.0.4)
                upper = (0, 0, patch(constraint) + 1)
            else:
                # ~0.2.3 = [0.2.3-0.3)
                upper = (major(constraint), minor(constraint) + 1)
            return VersionRange(constraint, upper, exclusive=True)

    # Use semver package's comparisons for everything else:

    # semver requires three version numbers
    if len(constraint) < 3:
        while len(constraint) < 3:
            constraint = constraint + (0,)
        constraint_str = constraint_str[0 : first_digit.start()] + ".".join(
            map(str, constraint)
        )

    # Convert special comparison strings to format accepted by `semver` library.
    constraint_str = constraint_str.replace("≥", ">=").replace("≤", "<=")
    constraint_str = re.sub(r"(^|\b)=\b", "==", constraint_str)

    return SemverMatcher(constraint_str)


class SemverMatcher:
    """Provides a utility for using `semver` package to do version matching.

    The `SemverMatcher` takes a `constraint_str` to represent a regex to
    determine if a version tuple matches the constraint.

    The matching is handled via the `semver` package.
    """

    def __init__(self, constraint_str):
        self.constraint_str = constraint_str

    def match(self, v):
        """Check if `v` matches the constraint"""
        while len(v) < 3:
            v = v + (0,)
        v_str = ".".join(map(str, v))
        v_ver = semver.VersionInfo.parse(v_str)
        return semver.VersionInfo.match(v_ver, self.constraint_str)

    def __eq__(self, rhs):
        return self.constraint_str == rhs.constraint_str

    def __repr__(self):
        return self.constraint_str


class VersionRange:
    """Represents a range of release versions.

    A `VersionRange` contains versions from a `lower` to `upper` bound
    which may be inclusive (default: `exclusive=False`) or exclusive (`exclusive=True`).

    A release version (represented by a tuple) can be checked to see if it
    falls within a `VersionRange`
    """

    def __init__(self, lower, upper, exclusive=False):
        self.lower = lower
        self.upper = upper
        self.exclusive = exclusive

    def match(self, v):
        """Check if `v` falls into the version range"""
        if self.exclusive:
            return self.lower <= v < self.upper
        else:
            return self.lower <= v <= self.upper

    def __eq__(self, rhs):
        return (
            self.lower == rhs.lower
            and self.upper == rhs.upper
            and self.exclusive == rhs.exclusive
        )

    def __repr__(self):
        return (
            "["
            + ".".join(map(str, self.lower))
            + "-"
            + ".".join(map(str, self.upper))
            + (")" if self.exclusive else "]")
        )
