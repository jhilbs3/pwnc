"""
This file contains all pwnc helper methods.
"""

from pwnc_exceptions import *

def _normalize_symbols(symbols : dict):
    """
    This function takes a dictionary of strings mapped to integers or a dict of
    strings mapped to strings and returns a dictionary of strings mapped to
    strings.

    @symbols: dict of strings mapped to integers or strings mapped to strings

    @returns: dict of strings mapped to strings
    """
    normalized_symbols = {}
    for key, val in symbols.items():
        if(isinstance(val, int)):
            val = hex(val)
        normalized_symbols[key] = val
    return normalized_symbols

def _reverse_normalize_symbols(symbols : dict):
    """
    This function takes a dictionary of strings mapped to integers or a dict of
    strings mapped to strings and returns a dictionary of strings mapped to
    integers.

    @symbols: dict of strings mapped to integers or strings mapped to strings

    @returns: dict of strings mapped to integers.
    """
    reversed_symbols = {}
    for key, val in symbols.items():
        if(isinstance(val, str)):
            val = int(val, 16)
        reversed_symbols[key] = val
    return reversed_symbols
