import os
import shutil
from path_Windows_to_Linux import *

direct_file_path = path_Windows_to_Linux(r'C:\Users\SceneryMC\PycharmProjects\PythonScript\n_image_downloader\n_site.txt')
n_images_path = path_Windows_to_Linux(r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n')

with open(direct_file_path) as f:
    ls = [[y.lstrip('#') for y in x.split()] for x in f.readlines()]

class_num = 0
class_folder = rf"{n_images_path}{os.sep}{class_num}"
os.mkdir(class_folder)
folder_list = os.listdir(n_images_path)
for subclass in ls:
    if not subclass:
        print(f"第{class_num}类完成！")
        class_num += 1
        class_folder = rf"{n_images_path}{os.sep}{class_num}"
        os.mkdir(class_folder)
        continue
    for folder in subclass:
        if folder in folder_list:
            shutil.move(rf"{n_images_path}{os.sep}{folder}", rf"{n_images_path}{os.sep}{class_num}", copy_function=shutil.copy)
        else:
            print(f"{folder}缺失！")
print(f"第{class_num}类完成，终止！")


