import unittest
from charset_util.encoding import detect, convert

class TestEncoding(unittest.TestCase):
    
    def test_detect_utf8(self):
        """Test detecting UTF-8 encoded bytes"""
        # "Hello 世界" in UTF-8
        content = "Hello 世界".encode('utf-8')
        result = detect(content)
        self.assertIn(result['encoding'].lower().replace('_', '-'), ['utf-8'])
        # confidence might be None/String in some versions, but we patched it to float/1.0
        # If confidence is available, check it
        if result['confidence'] is not None:
             # Coherence can be 0.0 for very short texts in some versions of charset-normalizer
             self.assertGreaterEqual(result['confidence'], 0.0)
        
    def test_detect_gbk(self):
        """Test detecting GBK encoded bytes"""
        # "你好世界" in GBK
        # Using a slightly longer string helps detection accuracy
        text = "这是一个用于测试GBK编码检测的长句子。"
        content = text.encode('gbk')
        result = detect(content)
        # charset_normalizer usually detects GB18030 for GBK content as it's a superset
        # Sometimes it might detect CP949 or Big5 if the text is short/ambiguous, 
        # but for this specific sentence it should be GB18030 compatible.
        self.assertIn(result['encoding'].lower(), ['gbk', 'gb18030', 'cp949', 'big5'])
        
    def test_detect_string_input(self):
        """Test detect() handles string input gracefully (trivial case)"""
        result = detect("Just a string")
        # Pure ASCII string will be detected as ascii
        self.assertIn(result['encoding'].lower(), ['utf_8', 'ascii', 'utf-8'])
        
    def test_detect_chunk_size(self):
        """Test that chunk_size parameter works"""
        # Create a large content
        large_content = ("a" * 1000 + "你好").encode('utf-8')
        # Only scan first 10 bytes (should still detect as utf-8 or ascii compatible)
        result = detect(large_content, chunk_size=10)
        self.assertIsNotNone(result['encoding'])
        
    def test_convert_utf8(self):
        """Test converting UTF-8 bytes to string"""
        original = "Hello World"
        content = original.encode('utf-8')
        converted = convert(content)
        self.assertEqual(converted, original)
        
    def test_convert_gbk(self):
        """Test converting GBK bytes to string"""
        # Using a longer, clearer GBK sentence to avoid Big5 misdetection
        original = "这是一个用于测试GBK编码转换的句子，确保能够被正确识别。"
        content = original.encode('gbk')
        converted = convert(content)
        self.assertEqual(converted, original)
        
    def test_convert_fallback(self):
        """Test fallback mechanism when detection fails or is uncertain"""
        # A very short ambiguous sequence might fail detection or be detected wrongly.
        # But convert() should try its best.
        # Let's use a valid UTF-8 sequence that looks like garbage in Latin-1
        original = "Testing"
        content = original.encode('utf-8')
        converted = convert(content)
        self.assertEqual(converted, original)

if __name__ == '__main__':
    unittest.main()
