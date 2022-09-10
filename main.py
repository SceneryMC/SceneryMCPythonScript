s = """目标文件和可执行文件可以有几种不同的格式 。在绝大 多数 SVr4 实现中都采用了 一 种
称作 ELF （原意为 “Extensible Linker Fonnat , 可扩展链接器格式”、现在代表 “Executable and
Linking Fonnat ， 可执行文件和链接格 式 ”)的格式。 在其他系统中，可执行 文件的格式是 COFF
(Common Ojbect-FiJe Fonnat, 普通目标文件格式） 。在 BSD UNIX 中（就像佛 具 有佛的本性
一样） ， a.out 文件具 有 a.out 格式。"""

ls = [c for c in s]
i = 1
while i < len(ls):
    if (not (0 <= ord(ls[i-1]) <= 127) or not(0 <= ord(ls[i+1]) <= 127)) and ls[i] == ' ':
        ls.pop(i)
    i += 1
print("".join(ls))
