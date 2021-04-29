import unittest
import pwnc
from pwnc_exceptions import *

class TestPWNC(unittest.TestCase):
    
    def test_valid_symbols(self):
        symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
        self.assertEqual(pwnc.query_build_id(symbols), 
                         "libc6_2.27-3ubuntu1.2_amd64")
    
    def test_valid_symbols_integers(self):
        symbols = {"strncpy": 0xdb0, "strcat": 0xd800}
        self.assertEqual(pwnc.query_build_id(symbols), 
                         "libc6_2.27-3ubuntu1.2_amd64")

    def test_valid_symbols_mixed(self):
        symbols = {"strncpy": "0xdb0", "strcat": 0xd800}
        self.assertEqual(pwnc.query_build_id(symbols), 
                         "libc6_2.27-3ubuntu1.2_amd64")

    def test_valid_buildid(self):
        desired_symbols = ["system", "strcat"]
        buildid = "libc6_2.27-3ubuntu1.2_amd64"
        results = pwnc.query(desired_symbols, buildid=buildid)
        self.assertEqual(results['strcat'], 0x9d800)
        self.assertEqual(results['system'], 0x4f4e0)

    def test_valid_query(self):
        symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
        desired_symbols = ["system", "strcat"]
        results = pwnc.query(desired_symbols, symbols)
        self.assertEqual(results['strcat'], 0x9d800)
        self.assertEqual(results['system'], 0x4f4e0)

    def test_valid_libc_download(self):
        symbols = {"strncpy": "0xdb0", "strcat": "0xd800"}
        libc = pwnc.get_libc(symbols)
        self.assertIn(b"__libc_start_main", libc)
    
    def test_valid_libc_download_integers(self):
        symbols = {"strncpy": 0xdb0, "strcat": 0xd800}
        libc = pwnc.get_libc(symbols)
        self.assertIn(b"__libc_start_main", libc)

    def test_invalid_libc_download(self):
        symbols = {"gross": "0"}
        self.assertRaises(PWNCResponseError, pwnc.get_libc, symbols)

if __name__ == "__main__":
    unittest.main()
