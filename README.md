# charset-util

A utility package for charset detection and conversion.

## Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/128645061/charset-util.git
```

## Usage

### Detect Encoding

```python
from charset_util import detect

# Detect from bytes
content = b'\xe4\xbd\xa0\xe5\xa5\xbd'  # "你好" in utf-8
result = detect(content)
print(result)
# Output: {'encoding': 'utf-8', 'confidence': 1.0, 'language': 'Chinese'}
```

### Convert Encoding

```python
from charset_util import convert

# Convert bytes to string (auto-detects source encoding)
content = b'\xc4\xe3\xba\xc3'  # "你好" in gb2312
text = convert(content)
print(text)
# Output: "你好"
```
