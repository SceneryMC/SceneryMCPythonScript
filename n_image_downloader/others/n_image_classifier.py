import json
import os
import shutil
from collections import Counter
from path_Windows_to_Linux import *

direct_file_path = path_Windows_to_Linux(r'C:\Users\SceneryMC\PycharmProjects\PythonScript\n_image_downloader\n_site.txt')
n_images_path = path_Windows_to_Linux(r'F:\存储\其它\SYNC\等待分类\新建文件夹')
artist_threshold = 0.6
tags_threshold = 0.6

with open(direct_file_path) as f:
    ls = [x.replace('#', '').split() for x in f.readlines() if x != '\n']
with open('../last_n_site.json') as f:
    d_all = json.load(f)

folder_list = os.listdir(n_images_path)
misc_folder_num = 0
for subclass in ls:
    artists = Counter()
    tags = Counter()
    for folder in subclass:
        artists.update([d_all[folder]['artist']])
        tags.update(d_all[folder]['tags'])

    if artists.most_common(1)[0][1] > len(subclass) * artist_threshold:
        artist = artists.most_common(1)[0][0]
        print(f"ARTIST - {artist}: {subclass}")
        artist_dir = rf"{n_images_path}/{artist}"
    elif tags.most_common(1)[0][1] > len(subclass) * tags_threshold:
        tag = [t[0] for t in tags.most_common(5)]
        print(f"TAGS - {tag}: {subclass}")
        artist_dir = rf"{n_images_path}/{' '.join(tag)}"
    else:
        print(f"MISC - {misc_folder_num}: {subclass}")
        artist_dir = rf"{n_images_path}/MISC{misc_folder_num}"
        misc_folder_num += 1

    os.mkdir(artist_dir)
    for folder in subclass:
        if folder in folder_list:
            shutil.move(rf"{n_images_path}/{folder}", artist_dir, copy_function=shutil.copy)
        else:
            print(f"{folder}缺失！")



