"""
This file contains all pwnc helper methods.
"""
from typing import Mapping

from .pwnc_exceptions import PWNCTypeError, PWNCArgumentError


def _check_dictionary_types(dictionary, key_types, val_types):
    """ make sure key,val types are in key_types and val_types """

    err_msg = "expected one of {} but arg is {}"

    for key,val in dictionary.items():
        if(not type(key) in key_types):
            raise PWNCArgumentError(err_msg.format(key_types, type(key)))
        if(not type(val) in val_types):
            raise PWNCArgumentError(err_msg.format(val_types, type(val)))

def _normalize_symbols(symbols: Mapping[str, any]) -> Mapping[str, str]:
    """ converts a dict of [str, any] to [str, str] """
    
    if(not isinstance(symbols, dict)):
        raise PWNCArgumentError(f'expected dictionary but got {type(symbols)}')
    
    normalized_symbols = {}
    for key, val in symbols.items():
        if(isinstance(val, int)):
            val = hex(val)
        if(isinstance(key, str) and isinstance(val, str)):
            normalized_symbols[key] = val
        else:
            raise PWNCTypeError(
                    f'expected str and str but got {type(key)} and {type(val)}')
    return normalized_symbols


def _reverse_normalize_symbols(
                        symbols: Mapping[str, any]) -> Mapping[str, int]:
    """ converts a dict of [str, any] to [str, int]"""
    
    if(not isinstance(symbols, dict)):
        raise PWNCArgumentError(f'expected dictionary but got {type(symbols)}')

    reversed_symbols = {}
    for key, val in symbols.items():
        if(isinstance(val, str)):
            val = int(val, 16)
        if(isinstance(key, str) and isinstance(val, int)):
            reversed_symbols[key] = val
        else:
            raise PWNCTypeError(
                    f'expected str and int but got {type(key)} and {type(val)}')
    return reversed_symbols
