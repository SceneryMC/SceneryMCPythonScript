import json

import requests
import re
import html

artists = {12074343: "Ampyx", 31973045: "CHPTRS", 12037010: "Vexento", 783446: "Dabin", 845098: "Lights & Motion",
           1046308: "Marcus Warner", 99093: "The Piano Guys", 45336:"Thomas Bergerson", 79757: "Tony Anderson",
           1019952: "TheFatRat", 1045123: "Alan Walker"}
album_per_page = 12
headers = {
        "Cookie": "_ga=GA1.2.2021007609.1602479334; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1602479334,1602673632; _gid=GA1.2.168402150.1602673633; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1602673824; kw_token=5LER5W4ZD1C",
        "csrf": "5LER5W4ZD1C",
        "Referer": f"https://music.163.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    }


def generate_tmp():
    d = {}
    for artist_name in artists.values():
        d[artist_name] = []
    return d


def get_newest_info():
    with open('results/netease_artist_works.json', encoding='utf-8') as f:
        artist_works = json.load(f)
    artist_works_tmp = generate_tmp()

    for aritst_id, artist_name in artists.items():
        print(artist_name, end="\t")
        r = requests.get(f"https://music.163.com/artist/album?id={aritst_id}&limit={album_per_page}&offset=0",
                         headers=headers)
        pages = r.text.count("zpgi")
        result = [html.unescape(x) for x in re.findall('<div class="u-cover u-cover-alb3" title="([^"]+)">', r.text)]
        for page in range(1, pages):
            r = requests.get(
                f"https://music.163.com/artist/album?id={aritst_id}&limit={album_per_page}&offset={page * album_per_page}",
                headers=headers)
            result.extend(
                html.unescape(x) for x in re.findall('<div class="u-cover u-cover-alb3" title="([^"]+)">', r.text))
        new = list(set(result) - set(artist_works[artist_name]))
        artist_works_tmp[artist_name] = new
        print(new)

    with open('results/netease_artist_works_tmp.json', 'w', encoding='utf-8') as f:
        json.dump(artist_works_tmp, f, ensure_ascii=False, indent=True)


def merge():
    with open('results/netease_artist_works.json', encoding='utf-8') as f:
        artist_works = json.load(f)
    with open('results/netease_artist_works_tmp.json', encoding='utf-8') as f:
        artist_works_tmp = json.load(f)

    for artist_name in artist_works:
        artist_works[artist_name].extend(artist_works_tmp[artist_name])

    with open('results/netease_artist_works.json', 'w', encoding='utf-8') as f:
        json.dump(artist_works, f, ensure_ascii=False, indent=True)


if __name__ == '__main__':
    get_newest_info()
    if input("更新") == 'y':
        merge()
