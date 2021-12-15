#!/bin/sh

echo "removing dist"
rm -rf dist

echo "removing all .egg-info"
find . -name "*.egg-info" -exec rm -r {} +

echo "removing all __pycache__"
find . -iname "__pycache__" -exec rm -r {} +

echo "starting build"
python3 -m build
