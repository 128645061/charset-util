import logging

# Set up default logger
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .encoding import detect, convert
from .recovery import repair_mojibake, decode_unicode_escapes
from .inspector import get_char_details, inspect_text, explain_mojibake

__version__ = "0.0.1"
__all__ = [
    "detect", 
    "convert", 
    "repair_mojibake", 
    "decode_unicode_escapes",
    "get_char_details",
    "inspect_text",
    "explain_mojibake"
]
