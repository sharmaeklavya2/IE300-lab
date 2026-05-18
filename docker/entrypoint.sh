#!/bin/bash
set -e

if [ -f /workspace/texlive-packages.txt ]; then
    echo "Installing packages from texlive-packages.txt ..."
    xargs tlmgr install < /workspace/texlive-packages.txt
fi

source /pyvenv/bin/activate

if [ -f /workspace/requirements.txt ]; then
    echo "Installing python packages from requirements.txt ..."
    pip install -r /workspace/requirements.txt
fi

exec "$@"
