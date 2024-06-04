import json
import os
import random

tmp_file_path = r'files'
tmp_keypoints_database = 'text_files/tmp_keypoints_database.pickle'
tmp_artist_database = 'text_files/tmp_artist_database.pickle'
tmp_duplicate_path = 'text_files/duplicates.txt'
last_log = 'text_files/last_n_site.json'
all_log = 'text_files/all_n_site.json'
download_list_file = 'text_files/n_site.txt'

sync_path = r"F:\存储\其它\SYNC"
artist_path = rf"{sync_path}\ARTIST"
artist_alias = 'text_files/artist_alias.json'

id_to_path = dict[str, str]
artist_to_id_to_path = dict[str, id_to_path]

with open(last_log) as f:
    info = json.load(f)
with open(artist_alias) as f:
    alias = json.load(f)


def generate_test_url():
    return f"https://nhentai.net/g/{random.randrange(400000, 450000)}"


def get_all_exist(root_path) -> id_to_path:
    d = {}
    for base, folder, files in os.walk(root_path):
        if not folder:
            name = os.path.basename(base)
            if name.isdigit() and 100 < int(name) < 1000000:
                d[name] = os.path.dirname(base)
    return d


def get_all_works_of_artists() -> artist_to_id_to_path:
    result = {}
    for rank in ["0", "3", "4", "5", "6"]:
        for artist in os.listdir(os.path.join(artist_path, rank)):
            result[artist] = get_all_exist(os.path.join(artist_path, rank, artist))
    return result
