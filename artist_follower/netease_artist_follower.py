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



update = True
for aritst_id, artist_name in artists.items():
    r = requests.get(f"https://music.163.com/artist/album?id={aritst_id}&limit={album_per_page}&offset=0",
                     headers=headers)
    pages = r.text.count("zpgi")
    result = []
    for page in range(pages):
        r = requests.get(f"https://music.163.com/artist/album?id={aritst_id}&limit={album_per_page}&offset={page * album_per_page}",
                         headers=headers)
        result.extend(html.unescape(x) for x in re.findall('<div class="u-cover u-cover-alb3" title="([^"]+)">', r.text))
    with open(f"netease_{artist_name}.json", encoding='utf-8') as f:
        j = json.load(f)
    if new := set(result) - set(j):
        print(f"新专辑：{new}")
        if update:
            with open(f"netease_{artist_name}.json", 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=True)

    # with open(f"netease_{artist_name}.json", 'w', encoding='utf-8') as f:
    #     f.write("[]\n")
