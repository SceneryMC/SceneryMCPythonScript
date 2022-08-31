import platform

t1 = ['%22C%3A%5CProgram%20Files%5CAdobe%5CAcrobat%20DC%5CAcrobat%5CAcrobat.exe%22%20/A%20%22page%3D', "evince -i "]
t2 = ['%3DOpenActions%22%20%22E%3A%5C%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%5C%E8%AE%A1%E7%AE%97%E6%9C%BA%5C%E5%8F%82%E8%80%83%E4%B9%A6%5C%E5%8F%AF%E8%83%BD%E4%BC%9A%E8%AF%BB%E7%9A%84%E4%B9%A6%5C%E7%AE%97%E6%B3%95%5C%E7%AE%97%E6%B3%95%E5%AF%BC%E8%AE%BA%5C4th%5CCLRS4th.pdf%22', " /mnt/E/学习资料/计算机/参考书/可能会读的书/算法/算法导论/4th/CLRS4th.pdf"]
address = [r'E:\学习资料\计算机\参考书\可能会读的书\算法\算法导论\整理\CLRS（复件）.mm', '/mnt/E/学习资料/计算机/参考书/可能会读的书/算法/算法导论/整理/CLRS（复件）.mm']

windows_to_linux = (platform.system().lower() == "linux")
with open(address[windows_to_linux], 'r') as f:
    content = f.read()
content = content.replace(t1[not windows_to_linux], t1[windows_to_linux])
content = content.replace(t2[not windows_to_linux], t2[windows_to_linux])
with open(address[windows_to_linux], 'w') as f:
    f.write(content)
# with open("/mnt/E/学习资料/计算机/参考书/可能会读的书/算法/算法导论/整理/CLRS.mm", 'r') as f:
#     content_original = f.read()
# print(content_original == content)

