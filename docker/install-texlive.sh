#!/bin/bash
set -e

# Install dependencies for the TeX Live installer
apt-get install -y --no-install-recommends wget perl xz-utils fontconfig ca-certificates make

# Download and extract the TeX Live installer
wget -qO /tmp/install-tl.tar.gz https://mirror.ctan.org/systems/texlive/tlnet/install-tl-unx.tar.gz
mkdir /tmp/install-tl
tar -xzf /tmp/install-tl.tar.gz --strip-components=1 -C /tmp/install-tl

# Run the installer and clean up
/tmp/install-tl/install-tl --profile /tmp/tl.profile
rm -rf /tmp/install-tl /tmp/install-tl.tar.gz

# Symlink the arch-specific bin directory to a fixed path
ln -s $(find /texlive/bin -mindepth 1 -maxdepth 1 -type d | head -1) /texlive/bin/active
