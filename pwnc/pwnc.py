
from typing import Mapping, List

from pwnc_urllib3 import _get_libc, _query, _query_symbols


def get_libc(known_symbols: Mapping[str, any] = {},
             buildid: str = "") -> bytes:
    """download libc by providing known symbols or a buildid

    Uses the libc.rip api to download a libc based on addresses of leaked
    symbols or a provided buildid. Symbols can be a dictionary of strings
    mapped to strings or strings mapped to integers.
    """

    return _get_libc(known_symbols=known_symbols, buildid=buildid)


def query(requested_symbols: List[str],
          known_symbols: Mapping[str, any] = {},
          buildid: str = "") -> Mapping[str, int]:
    """retrieve symbol addresses based on other known symbols or a buildid

    Uses the libc.rip api to retrieve the addresses of other known symbols
    within a given libc. This method can be called with either a buildid or a
    dictionary of symbols mapped to addresses (or both). The dictionary of
    symbols is a dictionary of strings mapped to strings or strings mapped to
    integers. Requested symbols are returned as a dictionary of strings mapped
    to integers.
    """

    # get the buildid if needed
    if(buildid == ""):
        buildid = query_build_id(known_symbols)

    # now get the desired symbols based on the buildid
    return _query_symbols(requested_symbols, buildid)


def query_build_id(symbols: Mapping[str, any]) -> str:
    """retrieve the buildid of a libc based on symbol addresses

    Uses the libc.rip api to retrieve the buildid of a given libc based on
    known symbol addresses. Symbols are passed as a dictionary of strings
    mapped to strings or strings mapped to integers.
    """

    return _query("id", symbols=symbols)


def query_download_url(symbols: Mapping[str, any], buildid: str = "") -> str:
    """retrieve the download url of a libc based on symbol addresses or buildid

    Uses the libc.rip api to retrieve a download url of a given libc based on
    symbol addresses. Symbols are passed as a dictionary of strings mapped to
    integers or strings mapped to strings.
    """

    return _query("download_url", symbols=symbols, buildid=buildid)
