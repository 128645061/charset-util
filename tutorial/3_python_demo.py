# Tutorial: Understanding Character Encodings with charset-util
# 教程：使用 charset-util 理解字符编码

import sys
import os

# Ensure we can import charset_util even if running from this subdirectory
# 确保在子目录运行时也能导入 charset_util
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

from charset_util import inspect_text, explain_mojibake

def main():
    print("==========================================")
    print("   Character Encoding Tutorial (Demo)   ")
    print("==========================================\n")

    # 1. Inspecting Characters (查看字符详情)
    print("1. Inspecting Characters")
    print("   Let's look at how '你好' is represented in different encodings.")
    print("   让我们看看 '你好' 在不同编码下是如何表示的。")
    
    text = "你好"
    report = inspect_text(text)
    print(report)
    print("\n   Key Takeaway (知识点):")
    print("   - Unicode is the ID (身份证号).")
    print("   - UTF-8/GBK are storage formats (存储格式).")
    print("   - Same character, different bytes! (同一个字，字节不同！)\n")

    # 2. Understanding Mojibake (理解乱码)
    print("2. Understanding Mojibake (乱码原理)")
    print("   What happens if we open a UTF-8 file with Latin-1 encoding?")
    print("   如果我们用 Latin-1 编码打开一个 UTF-8 文件会发生什么？")
    
    explanation = explain_mojibake("你好", source_encoding="utf-8", wrong_decoding="latin-1")
    print(explanation)
    
    print("\n   Another Example (另一个例子): GBK interpreted as UTF-8")
    explanation2 = explain_mojibake("你好", source_encoding="gbk", wrong_decoding="utf-8")
    print(explanation2)

if __name__ == "__main__":
    print("Welcome to the Character Encoding Tutorial!")
    main()
