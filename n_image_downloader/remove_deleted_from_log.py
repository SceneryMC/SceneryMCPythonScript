import json
import os
from maintain_artist import get_all_exist, tmp_path, artist_path


s1 = set(get_all_exist(artist_path).keys()) | set(os.listdir(tmp_path))
with open('all_n_site.json') as f:
    j = json.load(f)
s2 = set(j.keys())
s_diff = s2 - s1
print(s_diff)
for w in s_diff:
    del j[w]
    print(f"{w} deleted")
with open('all_n_site.json', 'w') as f:
    json.dump(j, f, ensure_ascii=False, indent=True)

with open('last_n_site.json') as f:
    j = json.load(f)
for w in s_diff:
    try:
        del j[w]
    except:
        print(f"FAILED {w}")
with open('last_n_site.json', 'w') as f:
    json.dump(j, f, ensure_ascii=False, indent=True)