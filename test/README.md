# pwnc test suite

This directory contains the tests used to determine the health and functionality
of pwnc's code.

## usage

From this repos root directory

    ./run_tests.sh

## methodology

There are many ways to test a library and its inner functionality. This project
is currently tested by feeding input to the exposed methods only. The idea
behind this is that interaction with the exposed methods is the only officially
supported way to use pwnc and therefore is the only part of pwnc that needs to
be actively checked. In the future we may decide to write test cases for every
method but for now this is what we've done. Some individual methods have test
cases because they are used frequently and hard to debug any other way.
