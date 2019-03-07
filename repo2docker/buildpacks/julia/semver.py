# This file implements the julia-specific logic for handling SemVer (Semantic
# Versioning) strings in .toml files.
#
# It uses the python "semver" package to do most version string comparisons, but
# the places where julia's SemVer handling differs from the semver package have
# been implemented directly.
#
# Here, we use tuples to represent a Version, and functors as "matchers". The matcher
# functors take a version string and return true if it passes its constraints.

import re
import semver

# Main algorithm:
# Create an AbstractMatcher instance from the constraint string, and check it
# against each version in the versions_list, returning the first success.
def find_semver_match(constraint, versions_list):
    matcher = create_semver_matcher(constraint)
    for vstr in reversed(versions_list):
        if matcher.match(str_to_version(vstr)):
            return vstr
    return None

def str_to_version(vstr):
    return tuple([int(n) for n in vstr.split('.')])

# --- Matcher interface -------------------------------------------

class AbstractMatcher:
    def match(self, v):
        pass

class SemverMatcher(AbstractMatcher):
    """ Match a version tuple to a given constraint_str using the `semver` package. """
    def __init__(self, constraint_str):
        self.constraint_str = constraint_str
    def match(self, v):
        while len(v) < 3:
            v = v+(0,)
        v_str = '.'.join(map(str, v))
        return semver.match(v_str, self.constraint_str)
    def __eq__(self, rhs):
        return self.constraint_str == rhs.constraint_str
    def __repr__(self):
        return self.constraint_str

# --- Custom matcher for julia-specific SemVer handling: ---------

from enum import Enum
class Exclusivity(Enum):
    EXCLUSIVE = 1
    INCLUSIVE = 2

class VersionRange(AbstractMatcher):
    """ Match a version tuple between lower and upper bounds. """
    def __init__(self, lower, upper, upper_exclusivity):
        self.lower = lower
        self.upper = upper
        self.upper_exclusivity = upper_exclusivity
    def match(self, v):
        if self.upper_exclusivity == Exclusivity.EXCLUSIVE:
            return self.lower <= v < self.upper
        else:
            return self.lower <= v <= self.upper
    def __eq__(self, rhs):
        return self.lower == rhs.lower and self.upper == rhs.upper and self.upper_exclusivity == rhs.upper_exclusivity
    def __repr__(self):
        return ("["+".".join(map(str, self.lower)) +"-"+ ".".join(map(str, self.upper)) +
                    (")" if self.upper_exclusivity == Exclusivity.EXCLUSIVE else "]"))

# Helpers
def major(v): return v[0]
def minor(v): return v[1] if len(v) >= 2 else 0
def patch(v): return v[2] if len(v) >= 3 else 0

# --- main constraint parser function ------------------------------------

def create_semver_matcher(constraint_str):
    """
    Returns a derived-class instance of AbstractMatcher that matches version
    tuples against the provided constraint_str.
    """
    constraint_str = constraint_str.strip()
    first_digit = re.search(r"\d", constraint_str)
    if not first_digit:
        # Invalid version string (no numbers in it)
        return ""
    constraint = str_to_version(constraint_str[first_digit.start():])

    comparison_symbol = constraint_str[0:first_digit.start()].strip()

    # Default to "^" search if no matching mode specified (up to next major version)
    if (first_digit.start() == 0) or (comparison_symbol == "^"):
        if major(constraint) == 0:
            # Also, julia treats pre-1.0 releases specially, as if the first
            # non-zero number is actually a major number:
            # https://docs.julialang.org/en/latest/stdlib/Pkg/#Caret-specifiers-1
            # So we need to handle it separately by bumping the first non-zero number.
            for i,n in enumerate(constraint):
                if n != 0 or i == len(constraint)-1: # (using the last existing number handles situations like "^0.0" or "^0")
                    upper = constraint[0:i] + (n+1,)
                    break
            return VersionRange(constraint, upper, Exclusivity.EXCLUSIVE)
        else:
            return VersionRange(constraint, (major(constraint)+1,), Exclusivity.EXCLUSIVE)

    # '~' matching (only allowed to bump the last present number by one)
    if (comparison_symbol == "~"):
        return VersionRange(constraint, constraint[:-1] +(constraint[-1]+1,), Exclusivity.INCLUSIVE)

    # Use semver package's comparisons for everything else:

    # semver requires three version numbers
    if len(constraint) < 3:
        while len(constraint) < 3:
            constraint = constraint+(0,)
        constraint_str = constraint_str[0:first_digit.start()] + ".".join(map(str, constraint))

    # Convert special comparison strings to format accepted by `semver` library.
    constraint_str = constraint_str.replace("≥", ">=").replace("≤", "<=")
    constraint_str = re.sub(r"(^|\b)=\b", "==", constraint_str)

    return SemverMatcher(constraint_str)
