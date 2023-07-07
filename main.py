# import os
# import shutil
# import random
# import fitz
import os
import re

import freeplane
from lxml import etree, html

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

# doc = fitz.open('/mnt/E/学习资料/计算机/参考书/可能会读的书/C++/入门/C++Primer/C++Primer5edCN（复件）.pdf')
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