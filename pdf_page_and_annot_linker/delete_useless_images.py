import re
import os
from mm_filelist import filelist
from path_Windows_to_Linux import path_Windows_to_Linux


for mm, _, _ in filelist.values():
    mm = path_Windows_to_Linux(mm)
    with open(mm) as f:
        content = f.read()
    used_images = re.findall(r"_files/(.*?\.png)", content)

    folder_path = os.path.normpath(f"{mm}/../{os.path.split(mm)[1][:-3]}_files")
    if os.path.exists(folder_path):
        all_images = os.listdir(folder_path)
        delete_list = set(all_images) - set(used_images)
        print(mm, delete_list)
        for image in delete_list:
            os.remove(f"{folder_path}/{image}")

