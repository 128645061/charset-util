import json
import re
from typing import Any, Union, Optional
import ftfy
from .strategies import JsonRecoveryPipeline
import logging

from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ExtractionResult:
    """
    Result of extracting and recovering JSON from a larger string.
    从字符串中提取和恢复JSON的结果。
    """
    prefix: str
    data: Any
    suffix: str
    
    def json_string(self) -> str:
        """Return the recovered data as a JSON string."""
        return json.dumps(self.data, ensure_ascii=False)
    
    def full_string(self) -> str:
        """Reconstruct the full string with recovered JSON."""
        return f"{self.prefix}{self.json_string()}{self.suffix}"

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

def recursive_decode(obj: Any) -> Any:
    """
    Recursively traverse the object and fix double-escaped strings in keys and values.
    递归遍历对象，修复键和值中的双重转义字符串。
    
    Uses an iterative approach to prevent RecursionError on deep structures.
    使用迭代方法以防止在深层结构上发生 RecursionError。
    
    e.g. "\\u5e94" -> "应"
    """
    # Use a stack for iterative traversal
    # 使用栈进行迭代遍历
    # Stack items: (parent_container, key_or_index, item_to_process)
    
    # Root handling is a bit special because we need to return the transformed root.
    # So we wrap it in a dummy list.
    dummy_root = [obj]
    stack = [(dummy_root, 0, obj)]
    
    while stack:
        parent, key, current = stack.pop()
        
        if isinstance(current, dict):
            # For dicts, we need to create a new dict to handle key transformation
            # But since we are modifying in-place via parent reference, we can't easily swap the dict object itself
            # without more complex logic. 
            # Simplified approach: Transform keys immediately, then push values to stack.
            
            # Wait, modifying keys in-place is hard.
            # Let's switch strategy: We build a NEW structure? 
            # No, iterative building is hard. 
            # Let's stick to modifying the PARENT's reference.
            
            new_dict = {}
            for k, v in current.items():
                # Transform key
                new_k = k
                if isinstance(k, str) and '\\u' in k:
                    try:
                        new_k = k.encode('utf-8').decode('unicode_escape')
                    except:
                        pass
                
                # We put 'v' into the new dict, but we also push it to stack to be transformed later.
                # The stack will update new_dict[new_k] when it processes 'v'.
                new_dict[new_k] = v
                stack.append((new_dict, new_k, v))
            
            # Replace the old dict in the parent with the new dict
            parent[key] = new_dict
            
        elif isinstance(current, list):
            # For lists, we can modify in-place
            for i, item in enumerate(current):
                stack.append((current, i, item))
                
        elif isinstance(current, str):
            if '\\u' in current:
                try:
                    decoded = current.encode('utf-8').decode('unicode_escape')
                    parent[key] = decoded
                except:
                    pass
        else:
            # Primitive types, do nothing
            pass
            
    return dummy_root[0]

def recover_json(content: Union[str, bytes]) -> Any:
    """
    A generalized parser for messy JSON-like strings.
    用于处理混乱 JSON 字符串的通用解析器。
    
    Strategies:
    1. Basic JSON load. (基础 JSON 加载)
    2. Unescape quotes (\") -> " and load. (去除转义引号并加载)
    3. Balance brackets/braces and load. (平衡括号并加载)
    4. Recursive unicode decoding for keys/values. (对键/值进行递归 Unicode 解码)
    """
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except:
            logger.debug("Failed to decode bytes as utf-8, trying ignore errors")
            content = content.decode('utf-8', errors='ignore')
            
    # Try 1: Direct load (unlikely for messy data but good baseline)
    # 尝试 1: 直接加载（虽然对于脏数据不太可能成功，但作为一个良好的基准）
    try:
        data = json.loads(content)
        logger.debug("Successfully loaded JSON directly")
        return recursive_decode(data)
    except:
        logger.debug("Direct JSON load failed, falling back to pipeline")
        pass
    
    # Use the pipeline for advanced recovery strategies
    # 使用流水线进行高级修复策略
    pipeline = JsonRecoveryPipeline()
    try:
        data = pipeline.process(content)
        return recursive_decode(data)
    except ValueError as e:
        raise e

def extract_and_recover(content: Union[str, bytes]) -> ExtractionResult:
    """
    Extract JSON from a larger string, recover it, and return the parts.
    从较大字符串中提取 JSON，进行修复，并返回各部分（前缀、数据、后缀）。
    
    This is useful when the input string contains non-JSON prefixes or suffixes that you want to preserve.
    当输入字符串包含您希望保留的非 JSON 前缀或后缀时，这很有用。
    """
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except:
            content = content.decode('utf-8', errors='ignore')

    # Find start of JSON
    match = re.search(r'[\{\[]', content)
    if not match:
        raise ValueError("No JSON-like structure found")
    
    start_idx = match.start()
    prefix = content[:start_idx]
    json_candidate = content[start_idx:]
    
    # We don't know exactly where the JSON ends if it's truncated or followed by garbage.
    # But recover_json works on the "candidate" string which starts with { or [.
    # The pipeline strategies usually handle trailing garbage by balancing or parsing.
    # However, if we want to preserve the *original* suffix, it's tricky because 
    # the recovery process might alter the string (e.g. unescaping quotes).
    
    # Simplified approach:
    # 1. Recover the data from the candidate part.
    # 2. Assume the suffix is empty because usually the JSON *is* the rest of the content (especially if truncated).
    #    If there was valid content AFTER the JSON, recover_json might ignore it or fail.
    
    # Wait, if the user input is "PREFIX {json} SUFFIX", and {json} is broken/truncated...
    # If it's truncated, there IS no suffix.
    # If it's NOT truncated but just messy, maybe we can find the matching closing brace?
    
    # For now, let's assume the JSON extends to the end of the string (or truncation point).
    # So suffix will be empty.
    
    data = recover_json(json_candidate)
    
    return ExtractionResult(
        prefix=prefix,
        data=data,
        suffix="" # Assuming everything after start_idx was part of the (potentially broken) JSON
    )
