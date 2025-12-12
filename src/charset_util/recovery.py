import ftfy
import re
from typing import List

def repair_mojibake(text: str) -> str:
    """
    Fix text that is broken due to encoding mix-ups (mojibake).
    修复因编码混淆（乱码）导致的损坏文本。
    
    This function uses ftfy (Fixes Text For You) to repair strings that were 
    decoded with the wrong encoding (e.g., utf-8 decoded as latin-1).
    此函数使用 ftfy 库来修复被错误解码的字符串（例如：将 UTF-8 误认为 Latin-1 解码）。
    
    Args:
        text: The string containing potential mojibake. (包含潜在乱码的字符串)
        
    Returns:
        The fixed string. (修复后的字符串)
    """
    return ftfy.fix_text(text)

def decode_unicode_escapes(text: str) -> str:
    """
    Extracts and decodes all Unicode escape sequences (like \\u4f60 or \\u0041) found in the text.
    Replaces the escape sequences with their corresponding characters.
    正则匹配文本中可以解析的 Unicode 转义序列（如 \\u4f60 或 \\u0041）并进行解析替换。
    
    This is useful for texts that contain raw unicode escapes mixed with other content.
    对于混合了原始 Unicode 转义符和其他内容的文本非常有用。
    
    Args:
        text: Input string containing potential unicode escapes.
        
    Returns:
        String with unicode escapes decoded.
    """
    # Pattern to match \u followed by 4 hex digits
    # We use a lambda in sub to decode each match individually
    
    # Logic:
    # 1. Match literal \u followed by 4 hex digits.
    # 2. Convert hex to char.
    # 3. Replace in string.
    
    def replace_match(match):
        escape_seq = match.group(0) # e.g. \u4f60
        try:
            # We encode to ascii (escaping non-ascii) then decode using unicode_escape
            # But simpler: just take the hex part and chr() it.
            hex_val = match.group(1)
            return chr(int(hex_val, 16))
        except:
            return escape_seq

    # Pattern: backslash u followed by 4 hex chars
    pattern = re.compile(r'\\u([0-9a-fA-F]{4})')
    
    return pattern.sub(replace_match, text)
