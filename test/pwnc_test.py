import unittest
import pwnc
from pwnc import pwnc
from pwnc.pwnc_exceptions import PWNCArgumentError, PWNCResponseError

class TestPWNC(unittest.TestCase):

    valid_symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
    invalid_symbols = {1: -1, 0: "hello"}
    invalid_symbol_addresses = {"strncpy": 0x0, "strcat": "0x1"}

    valid_request_symbols = ["printf", "system"]
    invalid_request_symbols = ["garbage", 1]

    valid_buildid = "d3cf764b2f97ac3efe366ddd07ad902fb6928fd7"
    invalid_buildid = "not a real buildid"

    valid_libcid = "libc6_2.27-3ubuntu1.2_amd64"
    invalid_libcid = "not a real libcid"

    # These tests are for get_libc

    def test_get_libc_valid_symbols(self):
        """ send valid symbols to get_libc """
        
        res = pwnc.get_libc(known_symbols=self.valid_symbols)
        self.assertTrue(isinstance(res, bytes))

    
    def test_get_libc_invalid_symbols(self):
        """ send invalid dictionary """
        
        self.assertRaises(PWNCArgumentError,
                          pwnc.get_libc,
                          self.invalid_symbols)
        
    
    def test_get_libc_invalid_symbol_addresses(self):
        """ send valid symbols but bad addresses """

        self.assertRaises(PWNCResponseError,
                          pwnc.get_libc,
                          self.invalid_symbol_addresses)

    # these tests are for query

    def test_query_valid_symbols(self):
        """ send valid symbols and retrieve a real dictionary of symbols """
        res = pwnc.query(self.valid_request_symbols, 
                         known_symbols=self.valid_symbols)
        self.assertTrue(isinstance(res, dict))

        # check to make sure all requested symbols were provided
        for sym in self.valid_requesat_symbols:
            self.assertTrue(sym in res)

    def test_query_valid_buildid(self):
        """ send a valid buildid and retrieve a real dictionary of symbols """
        res = pwnc.query(self.valid_request_symbols, buildid=self.valid_buildid)
        self.assertTrue(isinstance(res, dict))
        
        # check to make sure all requested symbols were provided
        for sym in self.valid_requesat_symbols:
            self.assertTrue(sym in res)

if __name__ == "__main__":
    unittest.main()
