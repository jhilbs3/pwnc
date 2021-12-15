import unittest
import src.pwnc.pwnc_helpers as pwnc_helpers
from src.pwnc.pwnc_exceptions import PWNCTypeError, PWNCArgumentError


class TestPWNCHelpers(unittest.TestCase):
    """ Tests the helper methods """

    valid_corpus = {"symbol": 100, "symbol2": "300", "symbol3": 400}
    invalid_corpus = {1: -1, "string": b"woops"}
    garbage_corpus = [1, "two", 3.0]

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
    

    def test_normalize_symbols_garbage(self):
        """ sends completely unexpected data to reverse_normalize """
        self.assertRaises(PWNCArgumentError,
                          pwnc_helpers._normalize_symbols,
                          self.garbage_corpus)


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


    def test_reverse_normalize_garbage(self):
        """ sends completely unexpected data to reverse_normalize """
        self.assertRaises(PWNCArgumentError,
                          pwnc_helpers._reverse_normalize_symbols,
                          self.garbage_corpus)


if __name__ == "__main__":
    unittest.main()
