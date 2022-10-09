Julia - REQUIRE, and use of old package manager
-----------------------------------------------

This tests a REQUIRE file for julia, using the repo2docker default version of
julia as specified in ``julia_require.py``. Note that this is default version is
0.6.4!

Starting with Julia v0.7 and up, the package manager has changed, so this tests
that the Julia version below that can be installed correctly as well.
