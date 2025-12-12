
import unittest
from charset_util.recovery import recover_json

class TestAdvancedRecovery(unittest.TestCase):
    def test_partial_truncation_unicode(self):
        """
        Test case for truncation happening in the middle of a unicode escape sequence.
        e.g. {"key": "val\\u4e
        """
        # "val\u4e" -> truncated at 'e', should be trimmed to "val" and closed
        raw = r'{"key": "val\u4e'
        result = recover_json(raw)
        self.assertEqual(result, {"key": "val"})

    def test_partial_truncation_escape(self):
        """
        Test case for truncation happening at backslash.
        e.g. {"key": "val\\
        """
        raw = r'{"key": "val' + "\\"
        result = recover_json(raw)
        self.assertEqual(result, {"key": "val"})

    def test_html_unescape(self):
        """
        Test case for JSON containing HTML entities.
        e.g. {&quot;key&quot;: &quot;value&quot;}
        """
        raw = r'{&quot;key&quot;: &quot;value&quot;}'
        result = recover_json(raw)
        self.assertEqual(result, {"key": "value"})

    def test_html_unescape_truncated(self):
        """
        Test case for HTML entities + truncation.
        """
        raw = r'{&quot;key&quot;: &quot;val'
        result = recover_json(raw)
        self.assertEqual(result, {"key": "val"})

if __name__ == '__main__':
    unittest.main()
