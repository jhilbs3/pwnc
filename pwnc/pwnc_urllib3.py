"""
This file contains all pwnc methods that make urllib3 calls.
"""

import urllib3
import json
from pwnc_exceptions import PWNCResponseError
from pwnc_helpers import _normalize_symbols, _reverse_normalize_symbols

LIBC_RIP_FIND = "https://libc.rip/api/find"
LIBC_RIP_LIBC = "https://libc.rip/api/libc/"

def _get_libc(known_symbols : dict):
    """
    This function will use the libc.rip api to download a libc based on
    addresses of leaked symbols.

    @known_symbols: dictionary of symbol names (strings) mapped to their
    addresses (strings or integers)

    @returns: a libc binary as a string of bytes
    """
    # takes a dictionary either {str:int} or {str:str} and returns a {str:str}
    normalized_symbols = _normalize_symbols(known_symbols)

    download_url = _query(normalized_symbols, "download_url")

    libc = None
    with urllib3.PoolManager() as http:
        r = http.request("GET", download_url)
        libc = r.data

    return libc

def _query(symbols : dict, desired_value : str):
    """
    This function querys https://libc.rip/api/find with a dictionary of symbols
    (strings) mappped to addresses (int). It returns the desired_value from the
    resulting json object

    @symbols: dictionary of symbol names (strings) mapped to addresses (strings
    or integers)

    @returns: the values assocaited with the desired_value key passed to this
    function
    """

    # make sure the dictionary passed to us is good
    normalized_symbols = _normalize_symbols(symbols)

    with urllib3.PoolManager() as http:

        # build the POST request and send it
        encoded_body = json.dumps({'symbols': normalized_symbols})
        response = http.request(
            'POST',
            LIBC_RIP_FIND,
            body = encoded_body,
            headers = {
                "Content-Type": "application/json"
            }
        )

        # parse the response
        parsed = json.loads(response.data.decode('utf-8'))
  
    try:
        return parsed[0][desired_value]
    except Exception as e:
        raise PWNCResponseError(
            f'Bad response from attempted query for {desired_value}. Response: {parsed}')

def _query_symbols(desired_symbols : list, buildid : str):
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
            body = encoded_body,
            headers = {
                "Content-Type": "application/json"
            }
        )

    parsed = json.loads(response.data.decode('utf-8'))
    
    try:
        return _reverse_normalize_symbols(parsed['symbols'])
    except Exception as e:
        raise PWNCResponseError(
            f'Bad response from attempted symbol query: {parsed}')

