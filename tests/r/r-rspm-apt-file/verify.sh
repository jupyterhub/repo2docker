#!/usr/bin/env bash
set -euo pipefail

apt list
apt list | grep libsodium-dev
