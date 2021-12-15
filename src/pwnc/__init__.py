"""retrieve libc binaries and symbol addresses based on other symbols

pwnc is a package used to query https://libc.rip for libc binaries, symbol
addresses, buildids, and more. This package is best used when attempting to
craft a memory corruption exploit that utilizes libc offsets or symbol
addresses.

The publicly exposed calls are:

get_libc           -- provide known symbols and their addresses and receive the
                      related libc as a byte string.

query              -- provide known symbol names mapped to their addresses.
                      Receive a dictionary of all symbols mappped to their
                      addresses.

query_buildid      -- provide known symbols mapped to their addresses and
                      receive the related libc buildid.

query_download_url -- provide known symbols mapped to their addresses and
                      receive the download url for the related libc.
"""

from typing import Mapping, List, Union

from .pwnc_urllib3 import _get_libc, _query, _query_symbols


def get_libc(known_symbols: Mapping[str, Union[str, int]] = {},
             buildid: str = "") -> bytes:
    """download libc by providing known symbols or a buildid

    Uses the libc.rip api to download a libc based on addresses of leaked
    symbols or a provided buildid. Symbols can be a dictionary of strings
    mapped to strings or strings mapped to integers.
    """

    return _get_libc(known_symbols=known_symbols, buildid=buildid)


def query(known_symbols: Mapping[str, Union[str, int]] = {},
          requested_symbols: List[str] = [],
          libcid: str = "") -> Mapping[str, int]:
    """retrieve symbol addresses based on other known symbols or a buildid

    Uses the libc.rip api to retrieve the addresses of other known symbols
    within a given libc. This method can be called with either a buildid or a
    dictionary of symbols mapped to addresses (or both). The dictionary of
    symbols is a dictionary of strings mapped to strings or strings mapped to
    integers. Requested symbols are returned as a dictionary of strings mapped
    to integers.
    """

    # get the libcid if needed
    if(libcid == ""):
        libcid = query_libc_id(known_symbols)

    # now get the desired symbols based on the buildid
    return _query_symbols(requested_symbols, libcid)


def query_build_id(symbols: Mapping[str, Union[str, int]]) -> str:
    """retrieve the buildid of a libc based on symbol addresses

    Uses the libc.rip api to retrieve the buildid of a given libc based on
    known symbol addresses. Symbols are passed as a dictionary of strings
    mapped to strings or strings mapped to integers.
    """

    return _query("buildid", symbols=symbols)


def query_libc_id(symbols: Mapping[str, Union[str, int]]):
    """retrieve the libcid of a libc based on symbol addresses

    Uses the libc.rip api to retrieve the libcid of a given libc based on known
    symbol addresses.
    """

    return _query("id", symbols=symbols)


def query_download_url(symbols: Mapping[str, Union[str, int]],
                       libcid: str = "") -> str:
    """retrieve the download url of a libc based on symbol addresses or buildid

    Uses the libc.rip api to retrieve a download url of a given libc based on
    symbol addresses. Symbols are passed as a dictionary of strings mapped to
    integers or strings mapped to strings.
    """

    return _query("download_url", symbols=symbols, libcid=libcid)
