def show_hex(data: bytes) -> str:
    return " ".join(f"{b:02X}" for b in data)

def main():
    char = "你"
    print(f"--- 分析字符: '{char}' ---")

    # 1. Unicode 层面 (内存中)
    # ord() 获取字符的整数编号
    code_point = ord(char)
    print(f"[Unicode] 码点编号: U+{code_point:04X} (十进制: {code_point})")
    print("说明: 这是字符的唯一身份证ID，与存储格式无关。\n")

    # 2. UTF-8 编码 (存储层面)
    utf8_bytes = char.encode('utf-8')
    print(f"[UTF-8]   字节流: {show_hex(utf8_bytes)}")
    print(f"          长度: {len(utf8_bytes)} 字节")
    print("说明: Unicode '4F60' 经过 UTF-8 算法计算，变成了 'E4 BD A0'。\n")

    # 3. GBK 编码 (存储层面)
    gbk_bytes = char.encode('gbk')
    print(f"[GBK]     字节流: {show_hex(gbk_bytes)}")
    print(f"          长度: {len(gbk_bytes)} 字节")
    print("说明: GBK 有自己的一套规则，'你' 被映射为 'C4 E3'。\n")

    # 4. 模拟乱码 (用错误的编码去解码)
    print("--- 乱码演示 ---")
    print(f"原始数据 (GBK): {show_hex(gbk_bytes)}")
    try:
        # 尝试强行用 utf-8 解析 gbk 的数据
        wrong_decode = gbk_bytes.decode('utf-8')
        print(f"用 UTF-8 强行解码: {wrong_decode}")
    except UnicodeDecodeError as e:
        print(f"用 UTF-8 强行解码: 失败 ({e})")
        print("原因: GBK 的字节 'C4' 在 UTF-8 规则中如果不符合后续字节格式，就会报错。")

    # Latin-1 (ISO-8859-1) 是一种单字节编码，它永远不会报错，但会把每个字节都当成一个字符
    latin1_decode = gbk_bytes.decode('latin-1')
    print(f"用 Latin-1 强行解码: {latin1_decode}")
    print("说明: 这就是典型的'古怪乱码'，原本的一个汉字变成了两个奇怪的西欧符号。")

if __name__ == "__main__":
    main()