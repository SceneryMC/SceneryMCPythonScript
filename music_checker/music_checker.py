from path_cross_platform import *
import json
import os

root_paths = [(r'F:\存储\音乐', 'storage'), (r'E:\时间的沉淀\音乐', 'collection')]
update = True

for root_path, name in root_paths:
    total = saved_total = 0
    with open(f'{name}_music_saved.json', encoding='utf-8') as f:
        music_saved_dict = json.load(f)

    music_new_dict = {}
    for root, folders, files in os.walk(path_fit_platform(root_path)):
        if os.sep == '\\':
            root = path_Windows_to_Linux(root)
        music_saved = set(music_saved_dict.get(root, []))
        music_ls = files
        music = set(music_ls)

        total += len(music)
        saved_total += len(music_saved)
        if music != music_saved:
            print(f"{root}:原有{len(music_saved)}，现有{len(music)}")
            if add := music - music_saved:
                print(f"增加：{add}")
            if remove := music_saved - music:
                print(f"减少：{remove}")
            print("")

        if update:
            music_new_dict[root] = music_ls

    if update:
        with open(f'{name}_music_saved.json', 'w', encoding='utf-8') as f:
            json.dump(music_new_dict, f, ensure_ascii=False, indent=True)

    print(f"----------------------------------------\n"
          f"{path_fit_platform(root_path)}：原有{saved_total}，现有{total}\n"
          f"----------------------------------------\n")
