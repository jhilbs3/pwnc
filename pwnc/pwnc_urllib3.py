"""
This file contains all pwnc methods that make urllib3 calls.
"""

import urllib3
import json
from typing import Mapping, List
from pwnc_exceptions import PWNCResponseError, PWNCArgumentError
from pwnc_helpers import _normalize_symbols, _reverse_normalize_symbols

LIBC_RIP_FIND = "https://libc.rip/api/find"
LIBC_RIP_LIBC = "https://libc.rip/api/libc/"


def _get_libc(known_symbols: Mapping[str, any] = {},
              buildid: str = "") -> bytes:
    """
    This function will use the libc.rip api to download a libc based on
    addresses of leaked symbols.

    @known_symbols: dictionary of symbol names (strings) mapped to their
    addresses (strings or integers)

    @returns: a libc binary as a string of bytes
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
    """
    This function querys https://libc.rip/api/find with a dictionary of symbols
    (strings) mappped to addresses (int). It returns the desired_value from the
    resulting json object

    @symbols: dictionary of symbol names (strings) mapped to addresses (strings
    or integers)

    @returns: the values associated with the desired_value key passed to this
    function
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
    """
    This function querys https://libc.rip/api/libc/<buildid> with a list of
    symbols (strings) and a buildid.

    @desired_symbols: list of strings. Each is a libc symbol
    @build: string id of the libc to query

    @returns: a dictionary of symbols (strings) mappped to their addresses
    (integers) If things go wrong an exception will be raised
    """

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
        return _reverse_normalize_symbols(parsed['symbols'])
    except Exception:
        raise PWNCResponseError(
            f'Bad response from attempted symbol query: {parsed}')
