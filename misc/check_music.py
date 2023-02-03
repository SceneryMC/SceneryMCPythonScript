from path_Windows_to_Linux import *
import json
import os

path_list = [(r'G:\音乐', 'all'), (r'G:\音乐\酷我音乐\song', 'kuwo')]
update = True

for path, name in path_list:
    music_ls = os.listdir(path_Windows_to_Linux(path))
    music = set(music_ls)
    with open(f'{name}_music_saved.json') as f:
        music_saved = set(json.load(f))
    print(f"{path}处的{name}：\n"
          f"增加：{music - music_saved}\n减少：{music_saved - music}")

    if update:
        with open(f'{name}_music_saved.json', 'w') as f:
            json.dump(music_ls, f)
