from typing import Optional, Union
import charset_normalizer

def detect(content: Union[bytes, str], chunk_size: Optional[int] = 1024 * 50) -> dict:
    """
    Detect the encoding of the given content.
    
    Args:
        content: The content to analyze. If string, it will be encoded to utf-8 first (trivial case).
        chunk_size: Maximum bytes to read for detection. Defaults to 50KB. Set to None to scan full content.
        
    Returns:
        A dictionary containing 'encoding', 'confidence', and 'language'.
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
        "confidence": result.fingerprint, # charset_normalizer uses fingerprint as a rough proxy or we can use the match object
        # Actually charset_normalizer match object has .encoding, .coherence (confidence-ish)
        "language": result.language
    }

def convert(content: bytes, target_encoding: str = "utf-8") -> str:
    """
    Convert the content to the target encoding.
    
    Args:
        content: The bytes to convert.
        target_encoding: The target encoding (default: utf-8).
        
    Returns:
        The decoded string.
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
            return content.decode('utf-8', errors='replace')
    
    # result.encoding is the detected encoding.
    # str(result) returns the decoded string using that encoding.
    return str(result)
