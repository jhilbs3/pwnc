#!/bin/bash

TESTS=test/*.py

for file in $TESTS
do
    echo "** RUNNING $file **"
    python3 -m unittest $file
done
