import unittest
from src import pwnc
from src.pwnc.pwnc_exceptions import (PWNCArgumentError,
                                      PWNCResponseError)

class TestPWNC(unittest.TestCase):

    valid_symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
    invalid_symbols = {1: -1, 0: "hello"}
    invalid_symbol_addresses = {"strncpy": 0x0, "strcat": "0x1"}

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


if __name__ == "__main__":
    unittest.main()
