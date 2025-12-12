import logging

# Set up default logger
logging.getLogger(__name__).addHandler(logging.NullHandler())

from .encoding import detect, convert
from .recovery import repair_mojibake, decode_unicode_escapes
