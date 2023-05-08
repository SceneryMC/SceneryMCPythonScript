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


# import os
# import shutil


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


# import random as rd
#
# ls_1 = [str(rd.randint(0, 9)) for _ in range(2000)]
# ls_2 = [str(rd.randint(0, 9)) for _ in range(2000)]
# i1 = int(''.join(ls_1))
# i2 = int(''.join(ls_2))
# print(i1)
# print(i2)
# print(i1 * i2)
# import random
#
# dis = ['Ubuntu', 'Fedora', 'ArchLinux', 'SUSE']
#
# with open('/home/scenerymc/code/test/foo.txt', 'w') as f:
#     for _ in range(200):
#         f.write(f"{random.choice(dis)}\t{random.randint(0, 12)}\t{random.randint(0, 12)}\t"
#                 f"{random.randint(1, 28)}/{random.randint(1, 12)}/{random.randint(2000, 2023)}\n")

# import fitz
#
#
# doc = fitz.open('/mnt/E/学习资料/计算机/参考书/可能会读的书/C++/入门/C++Primer/C++Primer5edCN（复件）.pdf')
# for page in doc:
#     for annot in page.annots():
#         if annot.colors['stroke'] == (1.0, 1.0, 0.0):
#             annot.set_opacity(0.05)
# doc.save('/mnt/E/学习资料/计算机/参考书/可能会读的书/C++/入门/C++Primer/C++Primer5edCN-tmp.pdf')
# import os
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

