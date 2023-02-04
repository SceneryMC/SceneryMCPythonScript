import os
import shutil

direct_file_path = '/mnt/F/存储/其它/SYNC/等待分类/新建文件夹 (6)/新建 文本文档.txt'
n_images_path = '/mnt/F/存储/其它/SYNC/等待分类/新建文件夹 (6)'

with open(direct_file_path) as f:
    ls = [[y.lstrip('#') for y in x.split()] for x in f.readlines()]

class_num = 0
class_folder = f"{n_images_path}/{class_num}"
os.mkdir(class_folder)
folder_list = os.listdir(n_images_path)
for subclass in ls:
    if not subclass:
        print(f"第{class_num}类完成！")
        class_num += 1
        class_folder = f"{n_images_path}/{class_num}"
        os.mkdir(class_folder)
        continue
    for folder in subclass:
        if folder in folder_list:
            shutil.move(f"{n_images_path}/{folder}", f"{n_images_path}/{class_num}", copy_function=shutil.copy)
        else:
            print(f"{folder}缺失！")
print(f"第{class_num}类完成，终止！")


