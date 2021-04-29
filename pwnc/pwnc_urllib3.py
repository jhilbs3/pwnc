"""
This file contains all pwnc methods that make urllib3 calls.
"""

import urllib3
import json
from typing import Mapping, List
from pwnc_exceptions import (PWNCResponseError,
                             PWNCArgumentError,
                             PWNCSymbolError)
from pwnc_helpers import _normalize_symbols, _reverse_normalize_symbols

LIBC_RIP_FIND = "https://libc.rip/api/find"
LIBC_RIP_LIBC = "https://libc.rip/api/libc/"


def _get_libc(known_symbols: Mapping[str, any] = {},
              buildid: str = "") -> bytes:
    """ download a given libc based on symbols or buildid

    Uses a dictionary of known symbols mapped to addresses or a buildid
    (or both). Symbols are strings mapped to strings or strings mapped to
    integers
    """

    # raise an exception if we aren't provided one ofof the arguments
    if(len(known_symbols) == 0 and len(buildid) == 0):
        raise PWNCArgumentError('buildid or symbol required')

    # takes a dictionary either {str:int} or {str:str} and returns a {str:str}
    normalized_symbols = _normalize_symbols(known_symbols)

    download_url = _query("download_url",
                          symbols=normalized_symbols,
                          buildid=buildid)

    libc = None
    with urllib3.PoolManager() as http:
        r = http.request("GET", download_url)
        libc = r.data

    if(not isinstance(libc, bytes)):
        raise PWNCResponseError("expected bytes object: {libc}")

    return libc


def _query(desired_value: str,
           symbols: Mapping[str, int] = {},
           buildid: str = "") -> any:
    """ retrieve symbol addresses based on symbols or buildid

    Uses known symbol addresses or a buildid to retrieve other symbol
    addresses. Symbols are a dict of strings mapped to integers or strings
    mapped to strings.
    """

    # raise an exception if we aren't provided one ofof the arguments
    if(len(symbols) == 0 and len(buildid) == 0):
        raise PWNCArgumentError('buildid or symbol required')

    # make sure the dictionary passed to us is good
    normalized_symbols = _normalize_symbols(symbols)

    with urllib3.PoolManager() as http:

        # build the POST request and send it
        to_dump = {}
        if(len(buildid) > 0):
            to_dump['buildid'] = buildid
        if(len(normalized_symbols) > 0):
            to_dump['symbols'] = normalized_symbols

        encoded_body = json.dumps(to_dump)

        response = http.request(
            'POST',
            LIBC_RIP_FIND,
            body=encoded_body,
            headers={"Content-Type": "application/json"}
        )

    try:
        # parse and return the response
        parsed = None
        parsed = json.loads(response.data.decode('utf-8'))
        return parsed[0][desired_value]
    except Exception:
        raise PWNCResponseError(
            f'attempted query for {desired_value}. Response: {parsed}')


def _query_symbols(desired_symbols: List[str],
                   buildid: str) -> Mapping[str, int]:
    """ makes the urllib3 call to retrieve symbols """

    with urllib3.PoolManager() as http:

        encoded_body = json.dumps({'symbols': desired_symbols})
        response = http.request(
            'POST',
            f"{LIBC_RIP_LIBC}{buildid}",
            body=encoded_body,
            headers={"Content-Type": "application/json"}
        )

    try:
        parsed = json.loads(response.data.decode('utf-8'))
        discovered_symbols = _reverse_normalize_symbols(parsed['symbols'])
    except Exception:
        raise PWNCResponseError(
            f'Bad response from attempted symbol query: {parsed}')

    # make sure all requested symbols exist in discovered_symbols
    for symbol in desired_symbols:
        if(symbol not in discovered_symbols):
            raise PWNCSymbolError(f'Requested symbol {symbol} not found')

    return discovered_symbols
