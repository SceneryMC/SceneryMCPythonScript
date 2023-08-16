import re
import os
import yaml
from path_cross_platform import path_fit_platform


with open('text_files/filelist.yaml', encoding='utf-8') as f:
    filelist = yaml.full_load(f)


for mm, _, _ in filelist.values():
    mm = path_fit_platform(mm)
    with open(mm, encoding='utf-8') as f:
        content = f.read()
    used_images = re.findall(r"_files/(.*?\.png)", content)

    folder_path = os.path.normpath(f"{mm}/../{os.path.split(mm)[1][:-3]}_files")
    if os.path.exists(folder_path):
        all_images = os.listdir(folder_path)
        delete_list = set(all_images) - set(used_images)
        print(mm, delete_list)
        for image in delete_list:
            os.remove(f"{folder_path}/{image}")

