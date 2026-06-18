#!/bin/bash
# Simple launcher for pyWebmConverter GUI on Linux/macOS
# Usage: chmod +x run.sh && ./run.sh

python3 -m pyWebmConverter "$@"
if [ $? -ne 0 ]; then
    echo ""
    echo "Error: Could not start pyWebmConverter"
    echo ""
    echo "Make sure you have:"
    echo "  1. Python 3.8+ installed"
    echo "  2. Run 'pip install -e .' to install the package"
    echo ""
fi
