import argparse
import json
import os.path
import pickle
from collections import defaultdict
from math import sqrt

import fitz
import freeplane
import lxml.etree
import yaml

# new_lines = []
# with open(r"C:\Users\SceneryMC\Source\Repos\assembly\first_window.asm") as f:
#     lines = f.readlines()
#     for line in lines:
#         if line == '\n':
#             new_lines.append("\n")
#             continue
#         line = line[:line.find(';')]
#         if line != "":
#             new_lines.append(f"{line}\n")
#
# with open(r"C:\Users\SceneryMC\Source\Repos\assembly\first_window.asm", 'w') as f:
#     f.writelines(new_lines)


# address = r"G:\收藏\图片\ESO\others"
# folders = ["_", "alma", "dsc", "ehpa", "img", "max", "uhd", "vista", "vlt"]
# filelist = os.listdir(address)
# print(filelist)
# for t in folders:
#     filelist.remove(t)
# for s in os.listdir(address):
#     for t in folders:
#         if s[:len(t)] == t:
#             shutil.move(rf"{address}\{s}", rf"{address}\{t}")


# ls_1 = [str(random.randint(0, 9)) for _ in range(2000)]
# ls_2 = [str(random.randint(0, 9)) for _ in range(2000)]
# i1 = int(''.join(ls_1))
# i2 = int(''.join(ls_2))
# print(i1)
# print(i2)
# print(i1 * i2)
#
# dis = ['Ubuntu', 'Fedora', 'ArchLinux', 'SUSE']
#
# with open('/home/scenerymc/code/test/foo.txt', 'w') as f:
#     for _ in range(200):
#         f.write(f"{random.choice(dis)}\t{random.randint(0, 12)}\t{random.randint(0, 12)}\t"
#                 f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(2000, 2023)}\n")

# doc = fitz.open('/mnt/E/学习资料/计算机/参考书/可能会读的书/C++/入门/C++Primer/C++Primer5edCN.pdf')
# page = doc[99]
# print(page.get_text("words"))
# for page in doc:
#     for annot in page.annots():
#         if annot.colors['stroke'] == (1.0, 1.0, 0.0):
#             annot.set_opacity(0.05)
# doc.save('/mnt/E/学习资料/计算机/参考书/可能会读的书/C++/入门/C++Primer/C++Primer5edCN-tmp.pdf')
#
# base = r'C:\Users\SceneryMC\Source\Repos\Project2\test1'
#
# for path in [x for x in os.listdir(base) if not x.startswith('log') and x.endswith('.log')]:
#     with open(f"{base}/{path}") as f:
#         content = f.readlines()
#     t = [x.strip(' \n').split(',') for x in content]
#     time = []
#     state = []
#     for x in t:
#         time.append(int(x[0]))
#         state.append(x[2].split('=')[-1])
#     # print(time)
#     # print(state)
#     print(time[-1] - time[0])
#     n, t = state.count('NEW'), state.count('TO')
#     print(len(state), n, t, n / (n + t))

# mm = freeplane.Mindmap(file)._mindmap
# with open(file) as f:
#     tree = etree.parse(f, parser=etree.XMLParser(load_dtd=True, no_network=False))
#     s = etree.tostring(tree.getroot().find('.//map'), encoding='utf-8')
# with open(file, 'w') as f:
#     f.write(s.decode('utf-8'))

# elements = []
# elements.extend(mm.xpath(".//*[re:match(text(), 'P\\d+-\\d+') and not(@LINK)]", namespaces={"re": "http://exslt.org/regular-expressions"}))
# elements.extend(mm.xpath(".//*[re:match(@TEXT, 'P\\d+-\\d+') and not(@LINK)]", namespaces={"re": "http://exslt.org/regular-expressions"}))
# for element in elements:
#     print(element.get("TEXT"), element.text)
# for elem in mm.iter():
#     print(elem.text, elem.get('TEXT'))
# r = re.search('(P(\\d+)-(\\d+))|(p(\\d+))', "P123-45")
# print(r.group(1), r.group(4))
# r = re.search('(P(\\d+)-(\\d+))|(p(\\d+))', "p1238123")
# print(r.group(1), r.group(4))

# result = []
# for root, folders, files in os.walk(r"F:\存储\其它\SYNC\ARTIST\0"):
#     if not files and folders:
#         result.append((os.path.basename(root), len(folders)))
# result.sort(key=lambda x:x[1], reverse=True)
# print(result)

# with open(path_fit_platform(r"E:\学习资料\bookxnote\notebooks\Java核心技术·卷I12ed\markups.json"), encoding='utf-8') as f:
#     s = f.read()
# ls = re.findall('"(fillcolor|linecolor)": "(\w{8})"', s)
# print([x[1] for x in ls])

# import lxml
#
#
# s = """<body style=\" font-family:'Microsoft YaHei UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.2.9 High-P<span style=\" font-weight:600;\">erforma</span></p>\n<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">nce</p></body>"""
# print(s)
# x = lxml.html.fromstring(s)
# print(x.text_content())
# s = '!@#$%^&*()_rdgqiwuoidiqwdj234567890"""'

# path = r"E:\学习资料\计算机\参考书\可能会读的书\C++\入门\C++Primer\C++Primer.mm"
#
# def unquot(r):
#     text = r.group()
#     xml_tree = lxml.etree.fromstring(text)
#     for t in xml_tree.iter():
#         if t.text:
#             t.text = html.unescape(t.text)
#     result = lxml.etree.tostring(xml_tree, encoding='utf-8').decode('utf-8')
#     return result
#
# with open(path, encoding='utf-8') as f:
#     s = f.read().replace("&nbsp;", "&#160;")
# s = re.sub(r"<p>.*?</p>", unquot, s, flags=re.DOTALL)
# with open(path, 'w', encoding='utf=8') as f:
#     f.write(s)

# mm = lxml.etree.parse('/home/scenerymc/.config/freeplane/1.11.x/templates/xmind2021_default.mm').getroot()
# styles = mm.find('.//map_styles')
# new_styles = lxml.etree.fromstring("<map_styles></map_styles>")
# styles.getparent().replace(styles, new_styles)
# print(lxml.etree.tostring(mm, encoding='utf-8').decode())

# with open('pdf_page_and_annot_linker/config.yaml') as f:
#     default_args = yaml.full_load(f)
# print(default_args['open_pdf_command']['Windows'])
# arg_parser = argparse.ArgumentParser()
# arg_parser.add_argument('--template', nargs='?', default=default_args['template'])
# arg_parser.add_argument('--filelist-entry', nargs='?', default=default_args['filelist_entry'])
# arg_parser.add_argument('--pdf', nargs='?', default=default_args['pdf'])
# arg_parser.add_argument('--mm', nargs='?', default=default_args['mm'])
# arg_parser.add_argument('--note', nargs='?', default=default_args['note'])
# arg_parser.add_argument('--color-to-style', nargs='*', default=default_args['color_to_style'])
# ns_args = arg_parser.parse_args()
# print(ns_args.color_to_style)

# with open('pdf_page_and_annot_linker/default_args.yaml') as f:
#     r = yaml.full_load(f)
# print(r)

# ls = [1,2,3,4,5,6]
# print(dict(zip(ls[0::2], ls[1::2])))

# mm = freeplane.Mindmap('/mnt/E/学习资料/计算机/参考书/可能会读的书/Java/入门/Java核心技术/Java核心技术卷1.mm')
# print(mm.styles)

# xml_tree = lxml.etree.fromstring('<test r="1" s="2"></test>')
# tag = xml_tree.get("s") or xml_tree.get('r')
# print(tag)

# d = {1: [2, 3, 3], 2: (34, 5, 6, 6, 7,)}
# print(max(d.values(), key=len))
# def np(n):
#     while n != 1:
#         print(n)
#         n = 3 * n + 1 if (n & 1) == 1 else n // 2
#
# np(27)

# import re
#
#
# SIZE = 8
# WIDTH = 128
# HEIGHT = 96
# tmp = [0] * ((WIDTH + 2) * (HEIGHT + 2))
# board = [0] * ((WIDTH + 2) * (HEIGHT + 2))
# num_to_char = ['▁▁', '▂▂', '▃▃', '▄▄', '▅▅', '▆▆', '▇▇', '██']
#
# def block(x, y):
#     if 0 <= (value := tmp[WIDTH * (x - 1) + (y - 1)]) <= 7:
#         return num_to_char[value]
#     else:
#         return f"{value:02}"
#
#
#
# def print_a_frame():
#     for x in range(1, HEIGHT + 1):
#         for y in range(1, WIDTH + 1):
#             print(block(x, y), end='')
#         print()
#
#
# with open(r'E:\学习资料\小学期\计组和汇编\cpu\testcases\lifegame\vmem.txt', encoding='utf-8') as f:
#     lines = f.readlines()
#
# for line in lines:
#     if 'NEW FRAME!' in line :
#         print(tmp)
#         print_a_frame()
#         print("--------------------------------------")
#     if (result := re.match("VMEM:(\w+), (\w+)", line)) is not None:
#         addr = int(result.group(1), base=16)
#         data = int(result.group(2), base=16)
#         tmp[addr] = data


# for line in lines:
#     if (result := re.match("DMEM:(\w+) at (\w+)", line)) is not None:
#         data = int(result.group(1), base=16)
#         addr = int(result.group(2), base=16)
#         if addr >= 16 + (SIZE + 2) ** 2:
#             tmp[addr - (16 + (SIZE + 2) ** 2)] = data
#         else:
#             board[addr - 16] = data
# for x in range(SIZE + 2):
#     for y in range(SIZE + 2):
#         print(board[(SIZE + 2) * x + y], end=' ')
#     print()
# print("----------------------------------------------")
# for x in range(SIZE + 2):
#     for y in range(SIZE + 2):
#         print(tmp[(SIZE + 2) * x + y], end=' ')
#     print()
# a = 678256785266743746749745991597595974957449495794595975499751974676434162672415672465747564276542567712546127651256742657215764256125641
#
#
# def sum_digits(a):
#     s = 0
#     for d in str(a):
#         s += int(d)
#     return s
#
#
# while a >= 10:
#     a = sum_digits(a)
# print(a)

import itertools as it

weapon = ['法器', '长枪', '单手剑', '大剑', '弓']
sex_and_age = ['成男', '少男', '成女', '少女', '萝莉']
rarity = ['四星', '常驻五星', '限定五星']
ability = ['主C', '副C', '辅助']
element = ['风', '岩', '雷', '草', '水', '火', '冰']


result = [''.join(t) for t in it.product(rarity, element, weapon, sex_and_age, ability)]
print(f"我们{'、'.join(result)}共{len(result)}推人怎么你了？？")

# with open(r'n_image_downloader/text_files/all_n_site.json') as f:
#     j = json.load(f)
# with open(r'n_image_downloader/text_files/artist_alias.json') as f:
#     alias = json.load(f)
# for work, work_info in j.items():
#     if 'artist' in work_info and work_info['artist'] in alias.keys():
#         print(work)

# primes = {2, 3, 5, 7, 11, 13, 17, 19}
# N = 10000000
# for n in range(2, N):
#     if all(n % p for p in primes if p < sqrt(n) + 1):
#         primes.add(n)
# print(sorted(primes))

path = os.path.join(r'F:\存储\其它\SYNC\ARTIST\0')
ls = []
for folder in os.listdir(path):
    if (p := len(os.listdir(os.path.join(path, folder)))) > 2:
        ls.append((folder, p))
ls.sort(key=lambda x: -x[1])
for folder, works in ls:
    print(f"{folder:20}, {works}")
