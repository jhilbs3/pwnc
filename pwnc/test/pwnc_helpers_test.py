import unittest
import pwnc_helpers
from pwnc_exceptions import PWNCTypeError


class TestPWNCHelpers(unittest.TestCase):
    """ Tests the helper methods """

    valid_corpus = {"symbol": 100, "symbol2": "300", "symbol3": 400}
    invalid_corpus = {1: -1, "string": b"woops"}

    def test_normalize_symbols_valid(self):
        """ test normalize symbols with a dict of str mapped to str and int """
        
        res = pwnc_helpers._normalize_symbols(self.valid_corpus)
        for key,val in res.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(val, str))


    def test_normalize_symbols_invalid(self):
        """ send invalid objects at noramlize symbols """
        
        self.assertRaises(PWNCTypeError,
                          pwnc_helpers._normalize_symbols,
                          self.invalid_corpus)

    def test_reverse_normalize_valid(self):
        """ send valid objects to reverse normalize symbols """

        res = pwnc_helpers._reverse_normalize_symbols(self.valid_corpus)
        for key,val in res.items():
            self.assertTrue(isinstance(key, str))
            self.assertTrue(isinstance(val, int))

    
    def test_reverse_normalize_invalid(self):
        """ send valid objects to reverse normalize symbols """

        self.assertRaises(PWNCTypeError,
                          pwnc_helpers._reverse_normalize_symbols,
                          self.invalid_corpus)

if __name__ == "__main__":
    unittest.main()
