from path_Windows_to_Linux import *
import json
import os

root_paths = [(r'F:\存储\音乐', 'storage'), (r'E:\时间的沉淀\音乐', 'collection')]
update = False

for root_path, name in root_paths:
    total = saved_total = 0
    with open(f'{name}_music_saved.json') as f:
        music_saved_dict = json.load(f)

    music_new_dict = {}
    for root, folders, files in os.walk(path_Windows_to_Linux(root_path)):
        root = path_Windows_to_Linux(root, not isLinux)
        music_saved = set(music_saved_dict.get(root, []))
        music_ls = files
        music = set(music_ls)

        total += len(music)
        saved_total += len(music_saved)
        if music != music_saved:
            print(f"{root}:原有{len(music_saved)}，现有{len(music)}")
            if music - music_saved:
                print(f"增加：{music - music_saved}")
            if music_saved - music:
                print(f"减少：{music_saved - music}")
            print("")

        if update:
            music_new_dict[root] = music_ls

    if update:
        with open(f'{name}_music_saved.json', 'w') as f:
            json.dump(music_new_dict, f)

    print(f"----------------------------------------\n"
          f"{path_Windows_to_Linux(root_path)}：原有{saved_total}，现有{total}\n"
          f"----------------------------------------\n")
