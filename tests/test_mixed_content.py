
import unittest
from charset_util.recovery import extract_and_recover

class TestMixedContent(unittest.TestCase):
    def test_prefix_and_truncation(self):
        """
        Test extracting and recovering JSON with a prefix and truncation.
        """
        raw = 'PREFIX: {"key": "val'
        result = extract_and_recover(raw)
        
        self.assertEqual(result.prefix, 'PREFIX: ')
        self.assertEqual(result.data, {"key": "val"})
        self.assertEqual(result.suffix, '')
        
        # Verify reconstruction
        # Note: json_string() will output valid JSON {"key": "val"}, so full string is 'PREFIX: {"key": "val"}'
        self.assertEqual(result.full_string(), 'PREFIX: {"key": "val"}')

    def test_user_case_with_prefix(self):
        """
        Test the specific user case with 'subject_name_map' prefix.
        """
        # Truncated version of user input
        raw = r"""'subject_name_map"{\"\\u5e94\\u7528\": 1"""
        
        result = extract_and_recover(raw)
        
        # The prefix is everything before the first {
        # Raw: 'subject_name_map"{\"\\u...
        # The first { is inside the quote... wait.
        # "{\"..." -> The first { is actually the one after "
        
        self.assertEqual(result.prefix, '\'subject_name_map"')
        # The JSON part is {\"\\u5e94\\u7528\": 1 -> which recovers to {"应用": 1}
        self.assertEqual(result.data, {"应用": 1})
        
    def test_nested_structure(self):
        raw = 'Data: [{"id": 1}, {"id": 2'
        result = extract_and_recover(raw)
        self.assertEqual(result.prefix, 'Data: ')
        self.assertEqual(result.data, [{"id": 1}, {"id": 2}])

if __name__ == '__main__':
    unittest.main()
