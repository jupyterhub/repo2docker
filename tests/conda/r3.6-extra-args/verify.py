#!/usr/bin/env python
import sys
import os

# conda should still be in /srv/conda
# and Python should still be in $NB_PYTHON_PREFIX
assert sys.executable == os.path.join(
    os.environ["NB_PYTHON_PREFIX"], "bin", "python"
), sys.executable
assert sys.executable.startswith("/srv/conda/"), sys.executable

# Repo should be in /srv/repo
assert os.path.exists("/srv/repo/verify.py")
assert os.path.abspath(__file__) == "/srv/repo/verify.py"

# Repo should be writable
assert os.access("/srv/repo", os.W_OK)
