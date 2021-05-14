import unittest
import pwnc
from pwnc import pwnc
from pwnc.pwnc_exceptions import (PWNCArgumentError,
                                  PWNCResponseError,
                                  PWNCSymbolError)

class TestPWNC(unittest.TestCase):

    valid_symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
    invalid_symbols = {1: -1, 0: "hello"}
    invalid_symbol_addresses = {"strncpy": 0x0, "strcat": "0x1"}

    valid_request_symbols = ["printf", "system"]
    invalid_request_symbols = ["garbage"]

    valid_libcid = "libc6_2.27-3ubuntu1.2_amd64"
    invalid_libcid = "not a real libcid"

    def test_query_valid_symbols(self):
        """ send valid symbols and retrieve a real dictionary of symbols """
        res = pwnc.query(self.valid_request_symbols, 
                         known_symbols=self.valid_symbols)
        self.assertTrue(isinstance(res, dict))

        # check to make sure all requested symbols were provided
        for sym in self.valid_request_symbols:
            self.assertTrue(sym in res)

    def test_query_valid_libcid(self):
        """ send a valid buildid and retrieve a real dictionary of symbols """
        res = pwnc.query(self.valid_request_symbols, libcid=self.valid_libcid)
        self.assertTrue(isinstance(res, dict))
        
        # check to make sure all requested symbols were provided
        for sym in self.valid_request_symbols:
            self.assertTrue(sym in res)

    def test_query_valid_libcid_and_symbols(self):
        """ send valid symbols and libcid for extra verbosity """
        
        res = pwnc.query(self.valid_request_symbols,
                         known_symbols=self.valid_symbols, 
                         libcid=self.valid_libcid)
        self.assertTrue(isinstance(res, dict))
        
        # check to make sure all requested symbols were provided
        for sym in self.valid_request_symbols:
            self.assertTrue(sym in res)

    def test_query_invalid_request_symbols(self):
        """ request symbols that do not exist. Expect a response exception """
       
        self.assertRaises(PWNCSymbolError,
                          pwnc.query,
                          self.invalid_request_symbols,
                          libcid=self.valid_libcid)

    def test_query_invalid_libcid(self):
        """ send a libcid that isnt real """

        self.assertRaises(PWNCResponseError,
                          pwnc.query,
                          self.valid_request_symbols,
                          libcid=self.invalid_libcid)


if __name__ == "__main__":
    unittest.main()
