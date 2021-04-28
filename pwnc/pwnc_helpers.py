"""
This file contains all pwnc helper methods.
"""
from typing import Mapping

from pwnc_exceptions import PWNCTypeError


def _normalize_symbols(symbols: Mapping[str, any]) -> Mapping[str, str]:
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
        if(isinstance(val, str)):
            normalized_symbols[key] = val
        else:
            raise PWNCTypeError(
                    f'expected an int or str but value is of type {type(val)}')
    return normalized_symbols


def _reverse_normalize_symbols(
                        symbols: Mapping[str, any]) -> Mapping[str, int]:
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
        if(isinstance(val, int)):
            reversed_symbols[key] = val
        else:
            raise PWNCTypeError(
                    f'expected an int or str but value is of type {type(val)}')
    return reversed_symbols
