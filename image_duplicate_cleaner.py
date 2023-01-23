import os
import itertools

root = r"F:\Huawei Share\Backup\HuaweiPhotos\myphone_EEEBE915B45C"
preferences = {
    ('Camera', '不错的照片'): 0,
    ('Screenshots', '无'): 0,
    ('旧手机截图', '膜蛤hath'): 0,
    ('膜蛤hath', '贴吧'): 1,
}

folders_listdir = os.listdir(root)
need_update = dict(zip(folders_listdir, [True] * len(folders_listdir)))
folders = {}
for folder in itertools.combinations(folders_listdir, 2):
    for i in range(2):
        if need_update[folder[i]]:
            folders[folder[i]] = set(os.listdir(rf"{root}\{folder[i]}"))
            need_update[folder[i]] = False
    duplicate = folders[folder[0]].intersection(folders[folder[1]])

    if len(duplicate) != 0:
        if folder not in preferences:
            print(f"{folder}: 新增重复对，请定义优先级！")
        else:
            folder_delete = folder[preferences[folder]]
            for file in duplicate:
                os.remove(rf"{root}\{folder_delete}\{file}")
                print(rf"{root}\{folder_delete}\{file}")
            need_update[folder_delete] = True

files = []
for _, _, file in os.walk(root):
    files.extend(file)
print(len(files), len(set(files)))
