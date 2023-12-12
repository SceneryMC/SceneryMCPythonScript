import json
import os
from maintain_artist import get_all_exist, artist_path, sync_path, info, alias
from n_image_downloader_fixed import all_log

classifiers = {
    'tags': {'time-stop', 'mind-control', 'mind-break', 'exhibitionism', 'bondage', 'tentacles', 'orgasm-denial',
             'fox-girl', 'yuri', 'full-color', 'cat-girl', 'bdsm', 'demon-girl', },
    'characters': {'cirno', 'flandre-scarlet', 'remilia-scarlet', 'patchouli-knowledge', 'reimu-hakurei', 'sakuya-izayoi'
                   'marisa-kirisame', 'yukari-yakumo', 'sanae-kochiya', 'momiji-inubashiri', 'yuuka-kazami',
                   'tenshi-hinanai', 'nue-houjuu', 'satori-komeiji', 'madoka-higuchi', 'yuuka-hayase', 'rin-tosaka', 'neeko',
                   'xiangling', 'hu-tao', 'furina', 'focalors'},
    'parodies': {'touhou-project', 'genshin-impact', 'arknights', 'blue-archive', 'league-of-legends'}
}
map_classifier_to_folder = {'tags': "TAG", "characters": "CHARACTER", 'parodies': "PARODY"}
local_path = get_all_exist(artist_path)


def valid_symlink(path):
    try:
        os.stat(path)
    except os.error:
        return False
    return True


def check_all_symlink(root_path):
    for base, _, files in os.walk(root_path):
        if artist_path in base:
            continue
        folders = os.listdir(base)
        for folder in folders:
            path = rf"{base}\{folder}"
            if os.path.islink(path) and not valid_symlink(path):
                os.remove(rf"{base}\{folder}")
                if folder in local_path:
                    os.symlink(rf"{local_path[folder]}\{folder}", rf"{base}\{folder}")
                    print(rf"UPDATED {path} to {local_path[folder]}\{folder}")
                else:
                    print(rf"DELETED {path}")


def add_symlink(artist, c, x, key):
    if not os.path.exists(p := rf"{sync_path}\{map_classifier_to_folder[c]}\{x}\{artist}"):
        os.makedirs(p)
    src, dst = rf"{local_path[key]}\{key}", rf"{p}\{key}"
    if not os.path.exists(dst):
        os.symlink(src, dst)
        print(rf"NEW {src} to {dst}")


def add_symlink_group(d, cl):
    for key, value in d.items():
        artist = alias.get(value['artist'], value['artist'])
        for c, ls in cl.items():
            real_value = value[c]
            if isinstance(real_value, list):
                matched = ls & set(real_value)
                for x in matched:
                    add_symlink(artist, c, x, key)
            elif real_value in ls:
                add_symlink(artist, c, real_value, key)


def add_new_classifiers():
    with open(all_log) as f:
        j = json.load(f)

    new_classifiers = {}
    for key, value in map_classifier_to_folder.items():
        new_classifiers[key] = classifiers[key] - set(os.listdir(f"{sync_path}/{value}"))
    if any(s for s in new_classifiers.values()):
        add_symlink_group(j, new_classifiers)
    add_symlink_group(info, classifiers)


if __name__ == '__main__':
    check_all_symlink(sync_path)
    add_new_classifiers()