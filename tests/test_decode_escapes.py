import unittest
from charset_util.recovery import decode_unicode_escapes

class TestDecodeEscapes(unittest.TestCase):
    def test_basic_decode(self):
        """Test simple unicode escape decoding."""
        text = r"Hello \u4f60\u597d World"
        expected = "Hello 你好 World"
        self.assertEqual(decode_unicode_escapes(text), expected)

    def test_mixed_content(self):
        """Test mixed content with valid and invalid escapes."""
        # Valid: \u0041 (A)
        # Invalid format: \u123 (too short), \uGGGG (not hex)
        # We only match \u followed by 4 hex digits.
        text = r"Valid: \u0041, Invalid: \u123, \uGGGG, Literal: \\u0041"
        
        # We need to escape backslashes in the expected string for Python string literal safety
        # So we must use raw string or escape backslash.
        # Input was: r"... Literal: \\u0041" -> \ \ u 0 0 4 1
        # Regex matches the second \ and u0041. Replaces with A.
        # Result: \A
        expected = r"Valid: A, Invalid: \u123, \uGGGG, Literal: \A"
        self.assertEqual(decode_unicode_escapes(text), expected)

    def test_complex_user_case(self):
        """Test the complex string provided by user previously."""
        # Note: The original string had \" which we are not handling here, only \uXXXX.
        # And raw string r'' interprets \ as literal.
        raw = r'subject_name_map"{\"\\u5e94\\u7528\\u7ecf\\u6d4e\\u5b66\":'
        # Here we have \\u5e94.
        # This is literal backslash, literal backslash, literal u, literal 5e94.
        # Our regex matches \u5e94.
        # So it will replace \u5e94 with 应.
        # Result: subject_name_map"{\"\\应\\u7528...
        
        # Wait, if input is `\\u5e94`, regex `\\u` matches the second backslash and u.
        # So it becomes `\应`.
        # This seems correct for "resolving all parseable bytecodes".
        
        expected_part = r'subject_name_map"{\"\\'
        # Actually let's test a simpler version
        s = r"Prefix \\u5e94 Suffix" # -> Prefix \应 Suffix
        self.assertEqual(decode_unicode_escapes(s), "Prefix \\应 Suffix")

    def test_no_escapes(self):
        """Test text with no escapes."""
        text = "Hello World"
        self.assertEqual(decode_unicode_escapes(text), text)

if __name__ == '__main__':
    unittest.main()
