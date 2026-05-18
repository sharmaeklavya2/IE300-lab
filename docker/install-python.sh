#!/bin/bash
set -e

apt-get install -y --no-install-recommends make python3 python3-venv

python3 -m venv /pyvenv
source /pyvenv/bin/activate
pip install numpy scipy matplotlib
