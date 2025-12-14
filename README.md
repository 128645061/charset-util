# charset-util 🔣

**The "Swiss Army Knife" for Character Encoding in Python.**  
**Python 字符编码处理的“瑞士军刀”。**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> "I just want this file to be readable, don't ask me about bytes."  
> "我只想让这个文件能读，别跟我扯什么字节。"

---

## 🎯 Positioning & Philosophy (定位与理念)

**charset-util** is not just a wrapper around `charset-normalizer` or `ftfy`. It is a **Facade (门面)** designed to solve the most common "encoding hell" scenarios with zero friction.

It positions itself as:
1.  **A Pragmatic Tool**: Unifies detection, conversion, and repair into a simple API.
2.  **An Educational Resource**: Includes a built-in `tutorial/` folder with interactive demos to help developers understand *why* their data is broken.

**Why use this?**
- ✅ **Simple**: No more `UnicodeDecodeError`.
- ✅ **Robust**: Auto-detects encoding, falls back gracefully, and even repairs mojibake.
- ✅ **Educational**: Learn encoding principles while fixing your bugs.

---

## 🏗 Architecture (架构)

The project follows a clean **Layered Architecture** with **Facade Pattern**:

```text
charset-util/
├── src/charset_util/       # [Core Layer]
│   ├── __init__.py         #   -> Facade: Exposes detect, convert, repair
│   ├── cli.py              #   -> Interface: CLI entry point
│   ├── encoding.py         #   -> I/O Logic: Handling Bytes <-> Str (Detect/Convert)
│   └── recovery.py         #   -> Text Logic: Handling Str <-> Str (Repair/Escape)
├── tutorial/               # [Education Layer]
│   ├── 1_concepts.md       #   -> Illustrated Guide
│   ├── 2_visualizer.html   #   -> Interactive HTML Tool
│   └── 3_python_demo.py    #   -> Runnable Python Scripts
└── tests/                  # [Quality Assurance]
```

- **Separation of Concerns**: `encoding.py` handles raw bytes (I/O boundary), while `recovery.py` handles pure text logic (Business logic).
- **Dependency Isolation**: Users interact with the high-level API, decoupling them from the underlying libraries (`charset-normalizer`, `ftfy`).

---

## 🚀 Installation

You can install this package directly from GitHub:

```bash
pip install git+https://github.com/128645061/charset-util.git
```

## 🛠 Usage

### 1. Detect Encoding (检测编码)
Don't guess. Let the tool tell you what's inside the box.

```python
from charset_util import detect

content = b'\xe4\xbd\xa0\xe5\xa5\xbd'  # "你好" in utf-8
result = detect(content)
print(result)
# Output: {'encoding': 'utf-8', 'confidence': 1.0, 'language': 'Chinese'}
```

### 2. Convert Encoding (转换编码)
Safely read any file into a Python string.

```python
from charset_util import convert

# Convert bytes to string (auto-detects source encoding)
content = b'\xc4\xe3\xba\xc3'  # "你好" in gb2312
text = convert(content)
print(text)
# Output: "你好"
```

### 3. Repair Mojibake (修复乱码)
Fix text that was decoded with the wrong encoding (e.g., UTF-8 read as Latin-1).

```python
from charset_util import repair_mojibake

# Broken text: "你好" (utf-8) decoded as latin-1
broken = "ä½ å¥½"
fixed = repair_mojibake(broken)
print(fixed)
# Output: "你好"
```

### 4. CLI Tool (命令行工具)

```bash
# Detect encoding
python -m charset_util.cli detect myfile.txt

# Convert file to UTF-8
python -m charset_util.cli convert raw.txt -o clean.txt

# Repair a broken file
python -m charset_util.cli repair broken.txt
```

---

## 📚 Learn Encodings (学习资源)

Check out the `tutorial/` folder in this repository for:
- **Illustrated Guide**: Understanding Unicode vs UTF-8 vs GBK.
- **Visualizer**: An HTML tool to see bytes in real-time.
- **Python Demo**: Run `py tutorial/3_python_demo.py` to see concepts in action.

---

## 📄 License

MIT License. Feel free to use in your projects.
