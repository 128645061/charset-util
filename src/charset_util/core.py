from typing import Optional, Union
import charset_normalizer
import ftfy

def detect(content: Union[bytes, str]) -> dict:
    """
    Detect the encoding of the given content.
    
    Args:
        content: The content to analyze. If string, it will be encoded to utf-8 first (trivial case).
        
    Returns:
        A dictionary containing 'encoding', 'confidence', and 'language'.
    """
    if isinstance(content, str):
        content = content.encode('utf-8')
        
    result = charset_normalizer.from_bytes(content).best()
    
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
    result = charset_normalizer.from_bytes(content).best()
    
    if result is None:
        # Fallback or error? For now let's try to decode with utf-8 or raise error
        return content.decode(target_encoding, errors='replace')
        
    return str(result)

def repair(text: str) -> str:
    """
    Fix text that is broken due to encoding mix-ups (mojibake).
    
    This function uses ftfy (Fixes Text For You) to repair strings that were 
    decoded with the wrong encoding (e.g., utf-8 decoded as latin-1).
    
    Args:
        text: The string containing potential mojibake.
        
    Returns:
        The fixed string.
    """
    return ftfy.fix_text(text)
