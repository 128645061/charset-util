# Tutorial: Understanding Unicode Escapes (\u4f60)
# 教程：理解 Unicode 转义序列 (\u4f60)

import re

def main():
    print("==========================================")
    print("   The Mystery of \\uXXXX (Unicode Escapes)   ")
    print("==========================================\n")

    raw_text = r"Hello \u4f60\u597d World"
    print(f"1. Input String (输入字符串):")
    print(f"   {raw_text}")
    print("   Notice that '\\u4f60' are just 6 separate characters here: \\, u, 4, f, 6, 0.")
    print("   注意：这里的 '\\u4f60' 仅仅是6个普通的字符。")

    print("\n2. How to Convert (转换原理):")
    
    # Step 1: Find the pattern
    print("   [Step 1] Find the pattern (寻找模式): '\\u' + 4 Hex Digits")
    pattern = re.compile(r'\\u([0-9a-fA-F]{4})')
    
    matches = pattern.findall(raw_text)
    print(f"   Found matches: {matches}")
    
    # Step 2: Parse Hex to Integer
    print("\n   [Step 2] Hex to Integer (十六进制转整数):")
    for hex_str in matches:
        int_val = int(hex_str, 16)
        print(f"   '{hex_str}' (Hex) -> {int_val} (Decimal)")
        
        # Step 3: Integer to Character
        char_val = chr(int_val)
        print(f"   [Step 3] Integer to Char (整数转字符):")
        print(f"   chr({int_val}) -> '{char_val}'")
        print("   ---")

    # Step 4: Final Result
    print("\n3. Final Replacement (最终替换结果):")
    decoded_text = pattern.sub(lambda m: chr(int(m.group(1), 16)), raw_text)
    print(f"   '{decoded_text}'")

    print("\n------------------------------------------")
    print("Quick Python Trick (Python 快捷技巧):")
    print("In Python, you can also use the 'unicode_escape' codec:")
    print("code: raw_text.encode('utf-8').decode('unicode_escape')")
    
    # Note: direct decode('unicode_escape') on string is deprecated in Python 3, 
    # usually we encode to latin-1 or ascii bytes first then decode.
    try:
        trick = raw_text.encode('utf-8').decode('unicode_escape')
        print(f"Result: '{trick}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("\\u4f60")
    print("\u4f60")
    main()
