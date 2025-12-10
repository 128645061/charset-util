import unittest
from charset_util import detect, convert, repair

class TestCharsetUtil(unittest.TestCase):
    def test_basic_functions_exist(self):
        """Test that core functions are importable."""
        self.assertTrue(callable(detect))
        self.assertTrue(callable(convert))
        self.assertTrue(callable(repair))

    def test_detect_utf8(self):
        """Test detection of UTF-8 content."""
        content = "这是一个比较长的中文句子，用于确保字符集检测能够准确识别为UTF-8编码。".encode('utf-8')
        result = detect(content)
        # charset-normalizer might return 'utf_8' or 'utf-8', normalize check
        self.assertIn(result['encoding'].replace('_', '-'), ['utf-8'])

    def test_convert(self):
        """Test conversion."""
        # GBK bytes for a longer sentence to ensure correct detection
        # "这是一个测试" (This is a test) in GBK
        content = "这是一个测试，用于测试GBK编码转换的准确性。".encode('gbk')
        text = convert(content)
        self.assertEqual(text, "这是一个测试，用于测试GBK编码转换的准确性。")

    def test_repair(self):
        """Test mojibake repair."""
        # Mojibake: "你好" (utf-8) interpreted as latin-1
        broken = "你好".encode('utf-8').decode('latin-1')
        fixed = repair(broken)
        self.assertEqual(fixed, "你好")

if __name__ == '__main__':
    unittest.main()
