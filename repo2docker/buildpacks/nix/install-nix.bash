#!/bin/bash
# This downloads and installs a pinned version of nix
set -ex

NIX_VERSION="2.3"
NIX_SHA256="e43f6947d1f302b6193302889e7800f3e3dd4a650b6f929c668c894884a02701"

# Do all our operations in /tmp, since we can't rely on current directory being writeable yet.
cd /tmp
wget --quiet https://nixos.org/releases/nix/nix-$NIX_VERSION/nix-$NIX_VERSION-x86_64-linux.tar.xz
echo "$NIX_SHA256  nix-$NIX_VERSION-x86_64-linux.tar.xz" | sha256sum -c
tar xJf nix-*-x86_64-linux.tar.xz
sh nix-*-x86_64-linux/install
rm -r nix-*-x86_64-linux*
