# pwnc
A python library for finding libc offsets based on leaked addresses. 
It utilizes the [libc-database](https://github.com/niklasb/libc-database) API.

## Installation

    pip3 install pwnc

## Usage

### get\_libc

Retrieve a libc in the form of a bytestring. Provide known symbol names mapped
to their addresses in memory. Not all symbol names are stored in the database.
Checkout [libc-database](https://github.com/niklasb/libc-database) for 
information on which symbols are stored.

    >>> import pwnc
    >>> known_addresses = {"strncpy": "0x7fffffff0db0",
                           "strcat": "0x7fffffffd800"}
    >>> libc_bytestring = pwnc.get_libc(known_addresses)
    >>> libc_bytestring[:4]
    b'\x7fELF'
    >>> 

### query

This method returns all known symbol offsets for a libc. Provide a dictionary
of symbol names mapped to their in memory offsets

    >>> import pwnc
    >>> known_addresses = {"strncpy": "0x7fffffff0db0",
                           "strcat": "0x7fffffffd800"}
    >>> symbols = pwnc.query(known_addresses)
    >>> for sym in symbols.items():
    ...     print(f"{sym[0]} = {hex(sym[1])}")
    ...
    __libc_start_main_ret = 0x21b97
    dup2 = 0x110ab0
    printf = 0x64f00
    puts = 0x80a30
    read = 0x110180
    str_bin_sh = 0x1b40fa
    system = 0x4f4e0
    write = 0x110250

