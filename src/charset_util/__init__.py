import logging

# Set up default logger
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .encoding import detect, convert
from .recovery import repair_mojibake, decode_unicode_escapes

__version__ = "0.0.1"
__all__ = [
    "detect", 
    "convert", 
    "repair_mojibake", 
    "decode_unicode_escapes"
]
