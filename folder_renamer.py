# import os
# import re
#
#
# def rank(x):
#     result = re.search(r"\d+", x)
#     if result is not None:
#         return int(result.group())
#     else:
#         return 0
#
#
# address = r"F:\存储\其它\新建文件夹\新建文件夹 (3)\劇毒少女\其它"
#
# for root, dirs, files in os.walk(address):
#     ls = os.listdir(root)
#     ls.sort(key=rank)
#
#     serial = 2
#     for file_name in ls:
#         if '新建文件夹 ' in file_name:
#             os.rename(rf"{root}\{file_name}", rf"{root}\新建文件夹 ({serial})")
#             serial += 1


import os
import re


def rank(x):
    result = re.search(r"\d+", x)
    if result is not None:
        return os.path.getmtime(os.path.join(root, x))
    else:
        return 0


address = r"F:\存储\其它\新建文件夹\新建文件夹 (3)\劇毒少女\SYNC\新建文件夹"

for root, dirs, files in os.walk(address):
    ls = os.listdir(root)
    if os.path.isfile(os.path.join(root, ls[0])):
        continue
    ls.sort(key=rank)
    # print(ls)

    serial = 2
    for file_name in ls:
        if '新建文件夹 ' in file_name:
            os.rename(rf"{root}\{file_name}", rf"{root}\新建文件夹 ({serial})xxx")
            serial += 1
for root, dirs, files in os.walk(address):
    for d in dirs:
        if 'xxx' in d:
            os.rename(rf"{root}\{d}", rf"{root}\{d.rstrip('xxx')}")
