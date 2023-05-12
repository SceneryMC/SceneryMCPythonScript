import os
import json
import re
import shutil


sync_path = r"F:\存储\其它\SYNC"
artist_path = rf"{sync_path}\ARTIST"
tmp_path = r"C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n"
with open('last_n_site.json') as f:
    info = json.load(f)
with open('artist_alias.json') as f:
    alias = json.load(f)

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
        if result := re.search(rf'\\ARTIST\\(\d)\\([\w-]+)$', base):
            d[result.group(2)] = int(result.group(1))
    return d


def move_folder_to_artist(from_root_path, to_root_path):
    local_path = get_all_exist(from_root_path)
    local_artist = get_artist_rank_exist(to_root_path)
    for key, value in info.items():
        artist = alias.get(value['artist'], value['artist'])
        rank = local_artist.get(artist, 0)
        if (dst := rf"{to_root_path}\ARTIST\{rank}\{artist}") not in local_path[key]:
            shutil.move(rf"{local_path[key]}\{key}", rf"{dst}\{key}")
            print(rf"{key} from {local_path[key]}\{key} to {dst}\{key}")
        else:
            print(f"UNTOUCHED {key} at {local_path[key]}")


def remove_empty_folder(root_path):
    for base, folder, files in os.walk(root_path):
        if not folder and not files:
            os.removedirs(base)


if __name__ == '__main__':
    move_folder_to_artist(tmp_path, artist_path)
    # remove_empty_folder(artist_path)
