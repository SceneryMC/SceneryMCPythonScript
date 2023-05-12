import os
from maintain_artist import get_all_exist, artist_path, sync_path, info, alias


classifiers = {
    'tags': {'time-stop', 'mind-control', 'mind-break', 'exhibitionism', 'bondage', 'tentacles', 'orgasm-denial',
             'fox-girl', 'yuri', 'full-color', 'cat-girl', 'bdsm', 'demon-girl'},
    'characters': {'cirno', 'flandre-scarlet', 'remilia-scarlet', 'patchouli-knowledge', 'reimu-hakurei', 'sakuya-izayoi'
                   'marisa-kirisame', 'yukari-yakumo', 'sanae-kochiya', 'momiji-inubashiri', 'yuuka-kazami',
                   'tenshi-hinanai', 'nue-houjuu', 'satori-komeiji', 'madoka-higuchi', 'yuuka-hayase', 'rin-tosaka'},
}
map_classifier_to_folder = {'tags': "TAG", "characters": "CHARACTER"}
local_path = get_all_exist(artist_path)

def valid_symlink(path):
    try:
        os.stat(path)
    except os.error:
        return False
    return True


def check_all_symlink(root_path):
    for base, folders, _ in os.walk(root_path):
        for folder in folders:
            path = rf"{base}\{folder}"
            if os.path.islink(path) and not valid_symlink(path):
                os.remove(rf"{base}\{folder}")
                os.symlink(rf"{local_path[folder]}\{folder}", rf"{base}\{folder}")
                print(f"UPDATED {path}")


def add_new_symlink():
    for key, value in info.items():
        artist = alias.get(value['artist'], value['artist'])
        for c, ls in classifiers.items():
            matched = ls & set(value[c])
            for x in matched:
                if not os.path.exists(p := rf"{sync_path}\{map_classifier_to_folder[c]}\{x}\{artist}"):
                    os.makedirs(p)
                src, dst = rf"{local_path[key]}\{key}", rf"{p}\{key}"
                if not os.path.exists(dst):
                    os.symlink(src, dst)
                    print(rf"NEW {src} to {dst}")


if __name__ == '__main__':
    check_all_symlink(sync_path)
    add_new_symlink()