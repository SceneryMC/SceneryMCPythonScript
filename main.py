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
import re

test = "fwiijfowiejofjiscreenqwdqwdqwd"
print(re.search(r"screen.*", test).group())

