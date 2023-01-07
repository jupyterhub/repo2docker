#!/bin/bash
# This downloads and installs a pinned version of nix
set -ex

NIX_VERSION="2.3.9"
if [ "$NIX_ARCH" = "aarch64" ]; then
  NIX_SHA256="733a26911193fdd44d5d68342075af5924d8c0701aae877e51a38d74ee9f4ff8"
else
  NIX_SHA256="49763fd7fa06bcb712ced2f3f11afd275e3a4d7bc5ff0d6fd1d50a4c3ce7bbf4"
fi

# Do all our operations in /tmp, since we can't rely on current directory being writeable yet.
cd /tmp
wget --quiet https://nixos.org/releases/nix/nix-$NIX_VERSION/nix-$NIX_VERSION-$NIX_ARCH-linux.tar.xz
echo "$NIX_SHA256  nix-$NIX_VERSION-$NIX_ARCH-linux.tar.xz" | sha256sum -c
tar xJf nix-*-$NIX_ARCH-linux.tar.xz
sh nix-*-$NIX_ARCH-linux/install
rm -r nix-*-$NIX_ARCH-linux*
