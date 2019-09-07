#!/bin/bash
# This downloads and installs a pinned version of nix
set -ex

NIX_VERSION="2.1.1"
NIX_SHA256="ad10b4da69035a585fe89d7330037c4a5d867a372bb0e52a1542ab95aec67999"

# Do all our operations in /tmp, since we can't rely on current directory being writeable yet.
cd /tmp
wget --quiet https://nixos.org/releases/nix/nix-$NIX_VERSION/nix-$NIX_VERSION-x86_64-linux.tar.bz2
echo "$NIX_SHA256  nix-2.1.1-x86_64-linux.tar.bz2" | sha256sum -c
tar xjf nix-*-x86_64-linux.tar.bz2
sh nix-*-x86_64-linux/install
rm -r nix-*-x86_64-linux*
