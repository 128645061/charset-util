import unittest
from charset_util import detect, convert

class TestCharsetUtil(unittest.TestCase):
    def test_import(self):
        self.assertTrue(callable(detect))
        self.assertTrue(callable(convert))

if __name__ == '__main__':
    unittest.main()
