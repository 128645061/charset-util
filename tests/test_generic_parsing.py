
import sys
import os

# Add src to path relative to this file
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from charset_util.recovery import recover_json

def test_user_case():
    print("--- Test 1: User's messy case ---")
    raw_input = r"""'subject_name_map"{\"\\u5e94\\u7528\\u7ecf\\u6d4e\\u5b66\": {\"id\": 1}, \"\\u7269\\u7406\\u5b66\": {\"id\": 2}, \"\\u5730\\u7406\\u5b66\": {\"id\": 3}, \"\\u54f2\\u5b66\": {\"id\": 4}, \"\\u7406\\u8bba\\u7ecf\\u6d4e\\u5b66\": {\"id\": 5}, \"\\u6cd5\\u5b66\": {\"id\": 6}, \"\\u653f\\u6cbb\\u5b66\": {\"id\": 7}, \"\\u793e\\u4f1a\\u5b66\": {\"id\": 8}, \"\\u6c11\\u65cf\\u5b66\": {\"id\": 9}, \"\\u9a6c\\u514b\\u601d\\u4e3b\\u4e49\\u7406\\u8bba\": {\"id\": 10}, \"\\u6559\\u80b2\\u5b66\": {\"id\": 12}, \"\\u5fc3\\u7406\\u5b66\": {\"id\": 13}, \"\\u4f53\\u80b2\\u5b66\": {\"id\": 14}, \"\\u4e2d\\u56fd\\u8bed\\u8a00\\u6587\\u5b66\": {\"id\": 15}, \"\\u5916\\u56fd\\u8bed\\u8a00\\u6587\\u5b66\": {\"id\": 16}, \"\\u65b0\\u95fb\\u4f20\\u64ad\\u5b66\": {\"id\": 17}, \"\\u8003\\u53e4\\u5b66\": {\"id\": 18}, \"\\u4e2d\\u56fd\\u53f2\": {\"id\": 19}, \"\\u4e16\\u754c\\u53f2\": {\"id\": 20}, \"\\u6570\\u5b66\": {\"id\": 21}, \"\\u5316\\u5b66\": {\"id\": 22}, \"\\u5929\\u6587\\u5b66\": {\"id\": 23}"""
    
    try:
        result = recover_json(raw_input)
        print("Success!")
        # Print a few items to verify decoding
        count = 0
        for k, v in result.items():
            print(f"{k}: {v}")
            count += 1
            if count >= 3:
                print("...")
                break
    except Exception as e:
        print(f"Failed: {e}")

def test_simple_truncation():
    print("\n--- Test 2: Simple Truncation ---")
    raw = '{"name": "test", "items": [1, 2, 3'
    try:
        result = recover_json(raw)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed: {e}")

def test_nested_truncation():
    print("\n--- Test 3: Nested Truncation ---")
    raw = '{"data": {"users": [{"id": 1, "name": "Alice"}, {"id": 2'
    try:
        result = recover_json(raw)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed: {e}")

def test_unicode_keys():
    print("\n--- Test 4: Unicode Keys ---")
    raw = r'{"\\u4f60\\u597d": "world"}'
    try:
        result = recover_json(raw)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    test_user_case()
    test_simple_truncation()
    test_nested_truncation()
    test_unicode_keys()
