"""
This file contains all pwnc helper methods.
"""
from typing import Mapping

from pwnc_exceptions import PWNCTypeError


def _normalize_symbols(symbols: Mapping[str, any]) -> Mapping[str, str]:
    """ converts a dict of [str, any] to [str, str] """

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
    """ converts a dict of [str, any] to [str, int]"""

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
