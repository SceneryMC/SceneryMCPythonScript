import os
import itertools

root = r"F:\Huawei Share\Backup\HuaweiPhotos\myphone_EEEBE915B45C"
preferences = {
    ('Camera', '不错的照片'): 0,
    ('Screenshots', '无'): 0,
    ('旧手机截图', '膜蛤hath'): 0,
    ('膜蛤hath', '贴吧'): 1,
    ('Camera', 'Recover'): 1,
}

folders_listdir = os.listdir(root)
folders = {}

for folder in folders_listdir:
    folders[folder] = set(os.listdir(rf"{root}\{folder}"))
for folder in itertools.combinations(folders_listdir, 2):
    duplicate = folders[folder[0]].intersection(folders[folder[1]])
    if len(duplicate) != 0:
        if folder not in preferences:
            print(f"{folder}: 新增重复对，请定义优先级！")
        else:
            folder_delete = folder[preferences[folder]]
            for file in duplicate:
                os.remove(rf"{root}\{folder_delete}\{file}")
                folders[folder_delete].remove(file)
                print(rf"{root}\{folder_delete}\{file}")

files = []
for _, _, file in os.walk(root):
    files.extend(file)
print(len(files), len(set(files)))
