postBuild and start
-------------------

This test checks that we can use a postBuild and start script
at the same time.

It also checks that exit on error (set -e) has not leaked into the main shell.
