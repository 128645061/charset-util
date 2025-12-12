
import unittest
import logging
import sys
from charset_util.recovery import extract_and_recover

# Configure logging to see debug output
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class TestSpecificUserCase(unittest.TestCase):
    def test_complex_truncated_string(self):
        # Constructing the string as provided by the user
        # Note: We use a raw string to handle backslashes conveniently, but we need to match the user's input structure.
        # User input: 'subject_name_map"{\"\\u5e94...
        
        # Let's reconstruct the start of the string
        # Prefix: 'subject_name_map"
        # JSON part starts with {
        # Keys are like \"\\u5e94...\" which means they are double escaped or just escaped quotes?
        # \" -> " in the final JSON key? No, standard JSON keys are "key".
        # If the input has \", it means the JSON string itself might be escaped.
        
        raw_part1 = r'subject_name_map"{\"\\u5e94\\u7528\\u7ecf\\u6d4e\\u5b66\": {\"id\": 1}, \"\\u7269\\u7406\\u5b66\": {\"id\": 2}, \"\\u5730\\u7406\\u5b66\": {\"id\": 3}, \"\\u54f2\\u5b66\": {\"id\": 4}, \"\\u7406\\u8bba\\u7ecf\\u6d4e\\u5b66\": {\"id\": 5}, \"\\u6cd5\\u5b66\": {\"id\": 6}, \"\\u653f\\u6cbb\\u5b66\": {\"id\": 7}, \"\\u793e\\u4f1a\\u5b66\": {\"id\": 8}, \"\\u6c11\\u65cf\\u5b66\": {\"id\": 9}, \"\\u9a6c\\u514b\\u601d\\u4e3b\\u4e49\\u7406\\u8bba\": {\"id\": 10}, \"\\u6559\\u80b2\\u5b66\": {\"id\": 12}, \"\\u5fc3\\u7406\\u5b66\": {\"id\": 13}, \"\\u4f53\\u80b2\\u5b66\": {\"id\": 14}, \"\\u4e2d\\u56fd\\u8bed\\u8a00\\u6587\\u5b66\": {\"id\": 15}, \"\\u5916\\u56fd\\u8bed\\u8a00\\u6587\\u5b66\": {\"id\": 16}, \"\\u65b0\\u95fb\\u4f20\\u64ad\\u5b66\": {\"id\": 17}, \"\\u8003\\u53e4\\u5b66\": {\"id\": 18}, \"\\u4e2d\\u56fd\\u53f2\": {\"id\": 19}, \"\\u4e16\\u754c\\u53f2\": {\"id\": 20}, \"\\u6570\\u5b66\": {\"id\": 21}, \"\\u5316\\u5b66\": {\"id\": 22}, \"\\u5929\\u6587\\u5b66\": {\"id\": 23}, \"\\'
        
        # The user input ends with \"\\  (indicating truncation at backslash)
        
        print(f"Testing with input length: {len(raw_part1)}")
        
        try:
            result = extract_and_recover(raw_part1)
            
            print(f"Prefix found: {result.prefix}")
            print(f"Data keys recovered: {list(result.data.keys())[:3]}...")
            
            # Assertions
            self.assertEqual(result.prefix, 'subject_name_map"')
            
            # Check a few specific keys
            # \u5e94\u7528\u7ecf\u6d4e\u5b66 -> 应用经济学
            self.assertIn("应用经济学", result.data)
            self.assertEqual(result.data["应用经济学"]["id"], 1)
            
            # \u7269\u7406\u5b66 -> 物理学
            self.assertIn("物理学", result.data)
            self.assertEqual(result.data["物理学"]["id"], 2)
            
            # Check the last complete item before truncation
            # \u5929\u6587\u5b66 -> 天文学 (id 23)
            self.assertIn("天文学", result.data)
            self.assertEqual(result.data["天文学"]["id"], 23)
            
            print("Successfully recovered data from truncated string!")
            
        except Exception as e:
            self.fail(f"Recovery failed with error: {e}")

if __name__ == '__main__':
    unittest.main()
