"""
This file contains all publicly exposed methods within pwnc. The private
methods are contained in all other files within this repository.

The publicly exposed calls are:

get_libc           -- provide known symbols and their addresses and receive the
                      related libc as a byte string.

query              -- provide requested symbol names and known symbol names
                      mapped to their addresses. Receive a dictionary of
                      requested symbols mappped to their addresses.

query_buildid      -- provide known symbols mapped to their addresses and
                      receive the related libc buildid.

query_download_url -- provide known symbols mapped to their addresses and
                      receive the download url for the related libc.
"""

from typing import Mapping, List

from pwnc_urllib3 import _get_libc, _query, _query_symbols


def get_libc(known_symbols: Mapping[str, any] = {},
             buildid: str = "") -> bytes:
    """
    This function will use the libc.rip api to download a libc based on
    addresses of leaked symbols.

    @known_symbols: dictionary of symbol names (strings) mapped to their
    addresses (strings or integers)

    @returns: a libc binary as a string of bytes
    """
    return _get_libc(known_symbols=known_symbols, buildid=buildid)


def query(requested_symbols: List[str],
          known_symbols: Mapping[str, any] = {},
          buildid: str = "") -> Mapping[str, int]:
    """
    This function uses the libc.rip api to attempt to find libc symbols based
    on leaked addresses.

    @known_symbols: dict of symbol names (strings) mapped to addresses (strings
    or integers)
    @request_symbols: list of requested symbols (strings)

    @returns: a dictionary of requested symbols (strings) mappped to their
    addresses (int). If things go wrong an exception will be raised
    """
    # TODO: This method must validate that the requested symbols  exist in the
    #      dictionary.

    # first get the buildid
    if(buildid == ""):
        buildid = query_build_id(known_symbols)

    # now get the desired symbols based on the buildid
    return _query_symbols(requested_symbols, buildid)


def query_build_id(symbols: Mapping[str, any]) -> str:
    """
    This funcion returns the 'id' (libc buildid) value from an API find call

    @symbols: dictionary of symbol names (strings) mapped to addresses (strings
    or integers)

    @returns: a build ID (string) that can be used too query symbol addresses.
    If things go wrong this function raises an execption.
    """
    return _query("id", symbols=symbols)


def query_download_url(symbols: Mapping[str, any], buildid: str = "") -> str:
    """
    This funcion returns the 'download_url' value from an API find call

    @symbols: dictionary of symbol names (strings) mapped to addresses (strings
    or integers)

    @returns: a download url (string) where the libc can be downloaded
    """
    return _query("download_url", symbols=symbols, buildid=buildid)
