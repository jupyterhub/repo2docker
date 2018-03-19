"""
Local builds respect .gitignore
Tests that files excluded in gitignore are not packaged inside the image
"""
import os
import subprocess
import tempfile
import time

GITIGNORE_CONTENT="""
*.csv
!A/0.csv
A/1.tsv
!/B/2.csv
B/1.tsv
C/
"""

VERIFY_SCRIPT="""
#!/usr/bin/env python
import os

assert os.path.exists("A/0.csv")
assert not os.path.exists("A/1.csv")
assert not os.path.exists("A/2.csv")

assert os.path.exists("A/0.tsv")
assert not os.path.exists("A/1.tsv")
assert os.path.exists("A/2.tsv")

assert not os.path.exists("B/0.csv")
assert not os.path.exists("B/1.csv")
assert os.path.exists("B/2.csv")

assert os.path.exists("B/0.tsv")
assert not os.path.exists("B/1.tsv")
assert os.path.exists("B/2.tsv")

assert not os.path.exists("C/0.csv")
assert not os.path.exists("C/1.csv")
assert not os.path.exists("C/2.csv")

assert not os.path.exists("C/0.tsv")
assert not os.path.exists("C/1.tsv")
assert not os.path.exists("C/2.tsv")
"""

def test_gitignore():
    """
    Local builds respect .gitignore
    """
    def create_directory_structure():
        # Create Directories and files
        #
        # It is important to create the directory structure programmatically
        # because if we include a folder with a .gitignore in the repository,
        # then git uses it to exclude files from being checked into
        # the repository
        for dirName in ['A', 'B', 'C']:
            os.mkdir(dirName)
            for file_ids in range(3):
                # Write csv
                fp = open(os.path.join(dirName, str(file_ids)+".csv"), "w")
                fp.write("test")
                fp.close()
                # Write .tsv
                fp = open(os.path.join(dirName, str(file_ids)+".tsv"), "w")
                fp.write("test")
                fp.close()
        # Create .gitignore
        with open(".gitignore", "w") as fp:
            fp.write(GITIGNORE_CONTENT)
        # Create a verify script
        with open("verify.py", "w") as fp:
            fp.write(VERIFY_SCRIPT)
            # Make the file executable
            mode = os.fstat(fp.fileno()).st_mode
            mode |= 0o111
            os.fchmod(fp.fileno(), mode & 0o7777)

    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        create_directory_structure()
        username = os.getlogin()
        euid = os.getegid()
        subprocess.check_output([
            'repo2docker',
            '--user-id', str(euid),
            '--user-name', username,
            tmpdir,
            'python',
            '/home/{}/verify.py'.format(username)
        ], stderr=subprocess.STDOUT)
