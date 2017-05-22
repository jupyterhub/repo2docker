## Builder

**Note**: The project will probably be renamed soon!

A simple commandline tool that builds a docker image off a git repository & pushes it to a docker registry.

It mostly relies on other tools ([Source to Image](https://github.com/openshift/source-to-image) or just docker)
for doing the actual building. It is a simple wrapper that does detection to figure out which
build method to use, and how to invoke that build method.
