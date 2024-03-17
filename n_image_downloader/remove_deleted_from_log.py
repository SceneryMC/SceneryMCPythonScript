import json
import os
import pickle
from maintain_artist import get_all_exist, tmp_file_path, artist_path
from n_image_downloader.clean_duplicates import database_path
from n_image_downloader_fixed import all_log, last_log


s1 = set(get_all_exist(artist_path).keys()) | set(os.listdir(tmp_file_path))
with open(all_log) as f:
    j = json.load(f)
s2 = set(j.keys())
s_diff = s2 - s1
print(s_diff)
for w in s_diff:
    del j[w]
    print(f"{w} deleted")
with open(all_log, 'w') as f:
    json.dump(j, f, ensure_ascii=False, indent=True)

with open(last_log) as f:
    j = json.load(f)
for w in s_diff:
    try:
        del j[w]
    except:
        print(f"FAILED {w}")
with open(last_log, 'w') as f:
    json.dump(j, f, ensure_ascii=False, indent=True)

with open(database_path, "rb") as f:
    database = pickle.load(f)
for w in s_diff:
    try:
        del database[w]
    except:
        print(f"PICKLE FAILED {w}")
with open(database_path, "wb") as f:
    pickle.dump(database, f)
