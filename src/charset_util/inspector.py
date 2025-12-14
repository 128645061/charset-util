from typing import List, Dict, Optional

def get_char_details(char: str) -> Dict[str, str]:
    """
    获取单个字符的详细编码信息。
    Get detailed encoding information for a single character.
    """
    if len(char) != 1:
        raise ValueError("Input must be a single character")

    code_point = ord(char)
    
    # UTF-8
    utf8_bytes = char.encode('utf-8')
    utf8_hex = ' '.join(f'{b:02X}' for b in utf8_bytes)
    
    # GBK (Not all chars support GBK)
    try:
        gbk_bytes = char.encode('gbk')
        gbk_hex = ' '.join(f'{b:02X}' for b in gbk_bytes)
    except UnicodeEncodeError:
        gbk_hex = "N/A (Not supported in GBK)"

    # Latin-1 (Usually fails for non-ascii, but useful for comparison)
    try:
        latin1_bytes = char.encode('latin-1')
        latin1_hex = ' '.join(f'{b:02X}' for b in latin1_bytes)
    except UnicodeEncodeError:
        latin1_hex = "N/A (Not supported in Latin-1)"

    return {
        "char": char,
        "unicode_point": f"U+{code_point:04X}",
        "unicode_int": str(code_point),
        "utf8_hex": utf8_hex,
        "utf8_len": str(len(utf8_bytes)),
        "gbk_hex": gbk_hex,
        "latin1_hex": latin1_hex
    }

def explain_mojibake(text: str, source_encoding: str, wrong_decoding: str) -> str:
    """
    模拟并解释乱码的产生过程。
    Simulate and explain how mojibake is generated.
    
    Example: explain_mojibake("你好", "utf-8", "latin-1")
    Means: "你好" encoded as utf-8, then decoded as latin-1.
    """
    try:
        raw_bytes = text.encode(source_encoding)
        raw_hex = ' '.join(f'{b:02X}' for b in raw_bytes)
        
        wrong_text = raw_bytes.decode(wrong_decoding, errors='replace')
        
        explanation = [
            f"--- Mojibake Analysis: '{text}' ---",
            f"1. Original Text: {text}",
            f"2. Encode as [{source_encoding}]:",
            f"   Bytes: {raw_hex}",
            f"3. Decode as [{wrong_decoding}]:",
            f"   Result: {wrong_text}",
            f"   Explanation: The byte sequence {raw_hex} was interpreted according to {wrong_decoding} rules."
        ]
        return "\n".join(explanation)
    except Exception as e:
        return f"Error simulating mojibake: {e}"

def inspect_text(text: str) -> str:
    """
    生成一段文本的详细编码分析报告。
    Generate a detailed encoding analysis report for a text.
    """
    report = []
    report.append(f"Analyzing Text: \"{text}\"")
    report.append("-" * 60)
    report.append(f"{'Char':<6} | {'Unicode':<10} | {'UTF-8 Bytes':<16} | {'GBK Bytes':<16}")
    report.append("-" * 60)
    
    for char in text:
        details = get_char_details(char)
        report.append(
            f"{details['char']:<6} | "
            f"{details['unicode_point']:<10} | "
            f"{details['utf8_hex']:<16} | "
            f"{details['gbk_hex']:<16}"
        )
    
    report.append("-" * 60)
    return "\n".join(report)
