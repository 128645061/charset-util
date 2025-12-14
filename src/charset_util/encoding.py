from typing import Optional, Union
import charset_normalizer

def detect(content: Union[bytes, str], chunk_size: Optional[int] = 1024 * 50) -> dict:
    """
    Detect the encoding of the given content.
    检测给定内容的编码。

    Use Case (场景):
    - When you receive a file (bytes) but don't know if it's UTF-8, GBK, or Latin-1.
    - 当你收到一个文件（字节流），但不知道它是 UTF-8、GBK 还是 Latin-1 编码时。
    - This corresponds to the "Guessing the Box" step in our tutorial.
    - 对应教程中“猜测包装盒”的步骤。
    
    Args:
        content: The content to analyze. If string, it will be encoded to utf-8 first (trivial case).
                 要分析的内容。如果是字符串，会先被编码为 utf-8（平凡情况）。
        chunk_size: Maximum bytes to read for detection. Defaults to 50KB. Set to None to scan full content.
                    检测时读取的最大字节数。默认为 50KB。设置为 None 则扫描全部内容。
        
    Returns:
        A dictionary containing 'encoding', 'confidence', and 'language'.
        包含 'encoding' (编码), 'confidence' (置信度), 和 'language' (语言) 的字典。
    """
    if isinstance(content, str):
        content = content.encode('utf-8')
    
    # Slice content if chunk_size is provided to avoid memory issues on large files
    scan_content = content
    if chunk_size is not None and len(content) > chunk_size:
        scan_content = content[:chunk_size]
        
    result = charset_normalizer.from_bytes(scan_content).best()
    
    if result is None:
        return {
            "encoding": None,
            "confidence": 0.0,
            "language": None
        }
        
    return {
        "encoding": result.encoding,
        # result.fingerprint is a SHA256 hash string in newer versions of charset-normalizer, not a float confidence!
        # result.coherence is what we might want for confidence-like metric if available, but it's not always exposed same way.
        # For now, let's just return 1.0 if we found a match, or use coherence if present.
        "confidence": getattr(result, 'coherence', 1.0),
        "language": result.language
    }

def convert(content: bytes, target_encoding: str = "utf-8") -> str:
    """
    Convert the content to the target encoding.
    将内容转换为目标编码。

    Use Case (场景):
    - When you want to safely read a file into a Python string (Unicode), regardless of its original encoding.
    - 当你想把文件安全地读成 Python 字符串（Unicode），而不在乎它原来是什么编码时。
    - This corresponds to the "Unpacking" step in our tutorial: auto-detect the box type and take out the character.
    - 对应教程中“拆快递”的步骤：自动识别盒子类型并取出字符。
    
    Args:
        content: The bytes to convert.
                 要转换的字节内容。
        target_encoding: The target encoding (default: utf-8).
                         目标编码（默认：utf-8）。
        
    Returns:
        The decoded string.
        解码后的字符串。
    """
    # For short content, charset_normalizer might be less accurate with GBK vs UTF-8
    # But here we trust it. 
    # NOTE: charset_normalizer.from_bytes returns a Matches object, .best() returns the best Match.
    # Match object has .output() method (or str(match)) which returns bytes decoded to str.
    
    result = charset_normalizer.from_bytes(content).best()
    
    if result is None:
        # Fallback: try to decode with target_encoding (usually utf-8), or try 'utf-8' with replace
        try:
            return content.decode(target_encoding)
        except:
            # If target encoding fails, try GB18030 (common for Chinese) before giving up to 'replace'
            try:
                return content.decode('gb18030')
            except:
                return content.decode('utf-8', errors='replace')
    
    # result.encoding is the detected encoding.
    # str(result) returns the decoded string using that encoding.
    try:
        return str(result)
    except:
        # If conversion fails even with detected encoding (rare but possible), fallback
        return content.decode('utf-8', errors='replace')
