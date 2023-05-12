import os
import json
import re
import shutil


def get_all_exist(root_path):
    d = {}
    for base, folder, files in os.walk(root_path):
        if not folder:
            name = base.split('\\')[-1]
            if name.isdigit() and 1000 < int(name) < 470000:
                d[name] = base[:base.rfind("\\")]
    return d


def get_artist_rank_exist(root_path):
    d = {}
    for base, folder, files in os.walk(root_path):
        if result := re.search(rf'\\新建文件夹\\(\d)\\([\w-]+)$', base):
            d[result.group(2)] = int(result.group(1))
    return d


def move_folder_to_artist(from_root_path, to_root_path):
    local_path = get_all_exist(from_root_path)
    local_artist = get_artist_rank_exist(to_root_path)
    with open('last_n_site.json') as f:
        d = json.load(f)
    with open('artist_alias.json') as f:
        a = json.load(f)
    for key, value in d.items():
        artist = a.get(value['artist'], value['artist'])
        if not artist or artist not in local_artist:
            level = 0
        else:
            level = local_artist[artist]
        if (dst := rf"{to_root_path}\新建文件夹\{level}\{artist}") not in local_path[key]:
            # shutil.move(rf"{local_path[key]}\{key}", rf"{dst}\{key}")
            print(rf"{key} from {local_path[key]}\{key} to {dst}\{key}")
        else:
            print(f"UNTOUCHED {key} at {local_path[key]}")


def remove_empty_folder(root_path):
    for base, folder, files in os.walk(root_path):
        if not folder and not files:
            os.removedirs(base)


if __name__ == '__main__':
    move_folder_to_artist(r"F:\存储\其它\SYNC", r"F:\存储\其它\SYNC")
    # remove_empty_folder("F:\存储\其它\SYNC")
