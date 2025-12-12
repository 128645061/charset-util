import json
import re
from typing import Any, Union, Optional
import ftfy
from .strategies import JsonRecoveryPipeline

def repair_mojibake(text: str) -> str:
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

def recursive_decode(obj: Any) -> Any:
    """
    Recursively traverse the object and fix double-escaped strings in keys and values.
    Uses an iterative approach to prevent RecursionError on deep structures.
    e.g. "\\u5e94" -> "应"
    """
    # Use a stack for iterative traversal
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
    
    Strategies:
    1. Basic JSON load.
    2. Unescape quotes (\") -> " and load.
    3. Balance brackets/braces and load.
    4. Recursive unicode decoding for keys/values.
    """
    if isinstance(content, bytes):
        try:
            content = content.decode('utf-8')
        except:
            content = content.decode('utf-8', errors='ignore')
            
    # Try 1: Direct load (unlikely for messy data but good baseline)
    try:
        return recursive_decode(json.loads(content))
    except:
        pass
    
    # Use the pipeline for advanced recovery strategies
    pipeline = JsonRecoveryPipeline()
    try:
        data = pipeline.process(content)
        return recursive_decode(data)
    except ValueError as e:
        raise e
