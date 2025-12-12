
import unittest
from charset_util.recovery import extract_and_recover

class TestUserCases(unittest.TestCase):
    def test_truncated_escaped_unicode_json(self):
        """
        Test case for a specific user scenario:
        Truncated JSON string with escaped quotes and double-escaped unicode characters.
        """
        raw_input = 'subject_name_map"{\"\\u5e94\\u7528\\u7ecf\\u6d4e\\u5b66\": {\"id\": 1}, \"\\u7269\\u7406\\u5b66\": {\"id\": 2}, \"\\u5730\\u7406\\u5b66\": {\"id\": 3}, \"\\u54f2\\u5b66\": {\"id\": 4}, \"\\u7406\\u8bba\\u7ecf\\u6d4e\\u5b66\": {\"id\": 5}, \"\\u6cd5\\u5b66\": {\"id\": 6}, \"\\u653f\\u6cbb\\u5b66\": {\"id\": 7}, \"\\u793e\\u4f1a\\u5b66\": {\"id\": 8}, \"\\u6c11\\u65cf\\u5b66\": {\"id\": 9}, \"\\u9a6c\\u514b\\u601d\\u4e3b\\u4e49\\u7406\\u8bba\": {\"id\": 10}, \"\\u6559\\u80b2\\u5b66\": {\"id\": 12}, \"\\u5fc3\\u7406\\u5b66\": {\"id\": 13}, \"\\u4f53\\u80b2\\u5b66\": {\"id\": 14}, \"\\u4e2d\\u56fd\\u8bed\\u8a00\\u6587\\u5b66\": {\"id\": 15}, \"\\u5916\\u56fd\\u8bed\\u8a00\\u6587\\u5b66\": {\"id\": 16}, \"\\u65b0\\u95fb\\u4f20\\u64ad\\u5b66\": {\"id\": 17}, \"\\u8003\\u53e4\\u5b66\": {\"id\": 18}, \"\\u4e2d\\u56fd\\u53f2\": {\"id\": 19}, \"\\u4e16\\u754c\\u53f2\": {\"id\": 20}, \"\\u6570\\u5b66\": {\"id\": 21}, \"\\u5316\\u5b66\": {\"id\": 22}, \"\\u5929\\u6587\\u5b66\": {\"id\": 23}, \"\\  (超过1000字符截断)'
        
        result = extract_and_recover(raw_input)
        
        # Verify specific keys exist and are correctly decoded
        self.assertIn("应用经济学", result.data)
        self.assertEqual(result.data["应用经济学"]["id"], 1)
        
        self.assertIn("物理学", result.data)
        self.assertEqual(result.data["物理学"]["id"], 2)
        
        self.assertIn("天文学", result.data)
        self.assertEqual(result.data["天文学"]["id"], 23)

if __name__ == '__main__':
    unittest.main()
