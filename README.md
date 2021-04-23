# pwnc
A python library for finding libc offsets based on leaked addresses. 
It utilizes this projects API https://github.com/niklasb/libc-database

## Installation
This project will be added as a pip3 module in the future. For now clone the
repo and move the pwnc/ folder to wherever you are keeping your python modules.

## Usage
There is currently only one method in this package that is important. First
create a dictionary that maps symbol names to known address. **addresses must be
strings**. Create a list of strings, one for each desired symbol.

    import pwnc
    desired_symbols = ["system", "strcat"]
    known_symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
    results = pwnc.query(desired_symbols, known_symbols)
    print(f"System = {hex(int(results['system'], 16))}")
    print(f"Strcat = {hex(int(results['strcat'], 16))}")

    $ python3 pwnc_example.py

