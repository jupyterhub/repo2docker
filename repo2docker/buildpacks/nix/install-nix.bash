#!/bin/bash
# This downloads and installs a pinned version of nix
set -ex

NIX_VERSION="2.13.2"
if [ "$NIX_ARCH" = "aarch64" ]; then
  NIX_SHA256="4ae275a46a2441d3459ae389a90ce6e8f7eff12c2a084b2d003ba6f8d0899603"
else
  NIX_SHA256="beaec0f28899c22f33adbe30e4ecfceef87b797278c5210ee693e22e9719dfb4"
fi

# Do all our operations in /tmp, since we can't rely on current directory being writeable yet.
cd /tmp
wget --quiet https://nixos.org/releases/nix/nix-$NIX_VERSION/nix-$NIX_VERSION-$NIX_ARCH-linux.tar.xz
echo "$NIX_SHA256  nix-$NIX_VERSION-$NIX_ARCH-linux.tar.xz" | sha256sum -c
tar xJf nix-*-$NIX_ARCH-linux.tar.xz
sh nix-*-$NIX_ARCH-linux/install
rm -r nix-*-$NIX_ARCH-linux*
