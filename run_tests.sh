#!/bin/bash

TESTS=test/*.py
SRC=src/pwnc/*.py

FLAKE8_PATH=$(which flake8)

if [ -z "$FLAKE8_PATH" ]
then
    echo "This project requires flake8"
    echo "You can find it at https://github.com/pycqa/flake8"
    exit 1
fi

echo "running unit tests"
for file in $TESTS
do
    echo "** RUNNING $file **"
    python3 -m unittest $file
done

echo "linting project"
for file in $SRC
do
    flake8 $file
done
