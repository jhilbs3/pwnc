"""retrieve libc binaries and symbol addresses based on other symbols

pwnc is a package used to query https://libc.rip for libc binaries, symbol
addresses, buildids, and more. This package is best used when attempting to
craft a memory corruption exploit that utilizes libc offsets or symbol
addresses.

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
