# Windows new lines in postBuild

A local git checkout of a postBuild file on a Windows host creates \r\n line
endings. When such a file is copied into the docker container it can't be
executed. This test checks that we always convert line endings to \n.

The postBuild in this directory is carefully crafted to have \r\n line endings
on all host operating systems.
