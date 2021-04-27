import urllib3
import json

LIBC_RIP_FIND = "https://libc.rip/api/find"
LIBC_RIP_LIBC = "https://libc.rip/api/libc/"

def get_libc(known_symbols : dict):
    """
    This function will use the libc.rip api to download a libc based on
    addresses of leaked symbols.

    @known_symbols: dictionary of symbol names (strings) mapped to their
    addresses (strings or integers)

    @returns: a libc binary as a string of bytes
    """
    # takes a dictionary either {str:int} or {str:str} and returns a {str:str}
    normalized_symbols = _normalize_symbols(known_symbols)

    download_url = _query_download_url(normalized_symbols)

    libc = None
    with urllib3.PoolManager() as http:
        r = http.request("GET", download_url)
        libc = r.data

    return libc

def query(requested_symbols : list, known_symbols : dict):
    """
    This function uses the libc.rip api to attempt to find libc symbols based
    on leaked addresses.

    @known_symbols: dict of symbol names (strings) mapped to addresses (strings
    or integers)
    @request_symbols: list of requested symbols (strings)

    @returns: a dictionary of requested symbols (strings) mappped to their
    addresses (int). If things go wrong an exception will be raised
    """
    results = {}

    # first get the buildid
    buildid = _query_build_id(known_symbols)

    # now get the desired symbols based on the buildid
    results = _query_symbols(requested_symbols, buildid)

    return results

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
    print(normalized_symbols)
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

def _query_build_id(symbols : dict):
    """
    This funcion returns the 'id' value from an API find call

    @symbols: dictionary of symbol names (strings) mapped to addresses (strings)

    @returns: a build ID (string) that can be used too query symbol addresses.
    If things go wrong this function raises an execption.
    """
    return _query(symbols, "id")

def _query_download_url(symbols : dict):
    """
    This funcion returns the 'download_url' value from an API find call

    @symbols: dictionary of symbol names (strings) mapped to addresses (strings
    or integers)

    @returns: a download url (string) where the libc can be downloaded
    """
    return _query(symbols, "download_url")

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
   
    return parsed[0][desired_value]

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

    return _reverse_normalize_symbols(parsed['symbols'])
