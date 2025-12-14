# 🆔 The Illustrated Guide to Character Encodings
# 字符编码图解指南

This document explains the relationship between Characters, Unicode, and Encodings (UTF-8, GBK) using simple analogies and icons.
本文档通过简单的比喻和图标，解释字符、Unicode 和编码（UTF-8, GBK）之间的关系。

---

## 1. The Core Concepts (核心概念)

### 🧩 Character (字符)
> The abstract idea of a symbol.
> 抽象的符号概念。

Examples: `A`, `你`, `😊`

### 🔢 Unicode (The ID System / 身份证系统)
> A giant list that assigns a unique number (Code Point) to every character in the world.
> 一个巨大的列表，为世界上的每一个字符分配一个唯一的数字（码点）。
> **It does NOT store the character. It just lists them.**
> **它不负责存储，只负责编号。**

| Char (字符) | Unicode Code Point (身份证号) |
| :---: | :--- |
| `A` | `U+0041` (65) |
| `你` | `U+4F60` (20320) |
| `😊` | `U+1F60A` (128522) |

---

## 2. Encoding: The Packaging Box (编码：包装盒)

> Encoding is the rule for turning the **Unicode Number** into **Bytes (0/1)** for storage.
> 编码是将 **Unicode 编号** 转换为 **字节（二进制）** 进行存储的规则。

Different encodings are like different sized boxes.
不同的编码就像不同尺寸的盒子。

### 📦 UTF-8 (The Smart Box / 智能变长盒子)
> The most popular encoding. It uses 1 byte for English, 3 bytes for Chinese.
> 最流行的编码。英文用1个字节，中文用3个字节。

- **Rule**:
    - `0xxxxxxx` (1 byte) -> ASCII
    - `1110xxxx 10xxxxxx 10xxxxxx` (3 bytes) -> Chinese

**Example: "你" (U+4F60)**
```text
Unicode:  0100 1111 0110 0000
             ↓
UTF-8:    [11100100] [10111101] [10100000]
Hex:      E4       BD       A0
```

### 📦 GBK (The Chinese Box / 中文专用盒子)
> An older encoding optimized for Chinese. Uses 2 bytes for Chinese.
> 针对中文优化的旧编码。中文通常用2个字节。

**Example: "你"**
```text
GBK Mapping: [11000100] [11100011]
Hex:         C4       E3
```

---

## 3. The Tragedy of Mojibake (乱码惨案) 💥

> Mojibake happens when you pack with one rule (e.g., UTF-8) but unpack with another (e.g., Latin-1).
> 当你用一种规则（如 UTF-8）打包，却用另一种规则（如 Latin-1）解包时，就会发生乱码。

### The Scenario (场景)
1. You save "你" using **UTF-8**.
   - Bytes: `E4 BD A0` (3 bytes)
   
2. You open it using **Latin-1** (ISO-8859-1).
   - Latin-1 is a simple encoding that maps **every single byte** to a character.
   - Latin-1 是单字节编码，它把**每一个字节**都对应到一个西欧字符。

### The Result (结果)

| Step | Data | Interpretation | Result |
| :--- | :--- | :--- | :--- |
| **Storage** | `E4` | Latin-1 Lookup -> `ä` | `ä` |
| **Storage** | `BD` | Latin-1 Lookup -> `½` | `½` |
| **Storage** | `A0` | Latin-1 Lookup -> ` ` (NBSP) | ` ` |

**Final Output**: `ä½ ` 
(Instead of "你")

### 🛠 How to Fix? (如何修复)
We need to reverse the process:
1. Take the mojibake string `ä½ `.
2. Encode it back to bytes using the **Wrong Encoding** (Latin-1) -> Get `E4 BD A0`.
3. Decode these bytes using the **Correct Encoding** (UTF-8) -> Get `你`.

```python
# The Fix
bad_string = "ä½ "
original_bytes = bad_string.encode('latin-1')  # b'\xe4\xbd\xa0'
good_string = original_bytes.decode('utf-8')   # "你"
```

---

## 4. Summary Table (总结表)

| System | Analogy (比喻) | Role (作用) |
| :--- | :--- | :--- |
| **Unicode** | ID Card Number (身份证号) | Defines WHAT the character is. |
| **UTF-8** | Flexible Shipping Box (伸缩快递盒) | Stores characters efficiently (Global standard). |
| **GBK** | Compact Chinese Box (紧凑中文盒) | Stores Chinese efficiently (Legacy standard). |
| **Mojibake** | Wrong Key for Lock (错误的钥匙) | Decoding bytes with the wrong rule. |
