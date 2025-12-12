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

### Data Recovery

`charset-util` provides powerful recovery tools for damaged or truncated data.

#### Recover Truncated/Escaped JSON

Useful when you have JSON logs that were cut off or double-escaped.

```python
from charset_util import recover_json

# Case 1: Truncated JSON
broken_json = '{"name": "test", "items": [1, 2, 3'
data = recover_json(broken_json)
print(data)
# Output: {'name': 'test', 'items': [1, 2, 3]}

# Case 2: Double-escaped Unicode in Keys
messy_json = r'{"\\u4f60\\u597d": "world"}'
data = recover_json(messy_json)
print(data)
# Output: {'你好': 'world'}
```

#### Repair Mojibake (Garbage Text)

Fixes text that has been decoded with the wrong encoding (e.g., UTF-8 decoded as Latin-1).

```python
from charset_util import repair_mojibake

# Mojibake: "你好" (utf-8) interpreted as latin-1
broken_text = "ä½\xa0å¥½"
fixed_text = repair_mojibake(broken_text)
print(fixed_text)
# Output: "你好"
```

## Why charset-util?

You might ask: *"Isn't this just `charset-normalizer` + `ftfy`?"*

Not exactly. While we stand on the shoulders of these giants, `charset-util` solves **engineering integration problems** that neither library handles alone:

| Feature | charset-normalizer | ftfy | charset-util |
|---------|-------------------|------|--------------|
| **Charset Detection** | ✅ Best in class | ❌ | ✅ (Wraps normalizer) |
| **Mojibake Repair** | ❌ | ✅ Best in class | ✅ (Wraps ftfy) |
| **Truncated JSON Repair** | ❌ | ❌ | ✅ **Core Feature** |
| **Nested/Double Escaping**| ❌ | ❌ | ✅ **Core Feature** |
| **One-Stop API** | ❌ | ❌ | ✅ |

*   **`charset-normalizer`** is the **Engine** (it runs).
*   **`ftfy`** is the **Bodywork** (it looks good).
*   **`charset-util`** is the **Car** (it drives you to the destination).

We handle the "dirty work" of combining these tools with custom heuristics to fix data that is both **structurally broken** (truncated JSON) and **content broken** (mojibake/escaped).
