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

import os

for root, folders, files in os.walk("/home/scenerymc/code/PycharmProjects/stable-diffusion-webui/outputs/outputs/meow/9/4/2/"):
    for i in range(len(files)):
        os.rename(f"{root}/{files[i]}", f"{root}/000{i}.png")
    for i in range(len(files)):
        os.rename(f"{root}/000{i}.png", f"{root}/{i}.png")
