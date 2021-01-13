#!/bin/bash
# This downloads and installs a pinned version of nix
set -ex

NIX_VERSION="2.3.9"
NIX_SHA256="49763fd7fa06bcb712ced2f3f11afd275e3a4d7bc5ff0d6fd1d50a4c3ce7bbf4"

# Do all our operations in /tmp, since we can't rely on current directory being writeable yet.
cd /tmp
wget --quiet https://nixos.org/releases/nix/nix-$NIX_VERSION/nix-$NIX_VERSION-x86_64-linux.tar.xz
echo "$NIX_SHA256  nix-$NIX_VERSION-x86_64-linux.tar.xz" | sha256sum -c
tar xJf nix-*-x86_64-linux.tar.xz
sh nix-*-x86_64-linux/install
rm -r nix-*-x86_64-linux*
