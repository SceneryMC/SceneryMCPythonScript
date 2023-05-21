import html
import json
import requests
from urllib.parse import quote, unquote


songs_per_page = 50
update = True


def get_response(encodName, page):
    referer = f'https://www.kuwo.cn/search/list?key={encodName}'
    url = f'https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={encodName}&pn={page}&rn={songs_per_page}&httpsStatus=1'
    headers = {
        "Cookie": "_ga=GA1.2.2021007609.1602479334; Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1602479334,1602673632; _gid=GA1.2.168402150.1602673633; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1602673824; kw_token=5LER5W4ZD1C",
        "csrf": "5LER5W4ZD1C",
        "Referer": f"{referer}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36",
    }
    return requests.get(url=url, headers=headers)


def check_an_artist(artist):
    response = json.loads(get_response(quote(artist), 1).text)["data"]
    total = int(response['total'])
    ls = []
    for i in range(2, 1 + total // songs_per_page + int(total % songs_per_page != 0)):
        ls.extend([(html.unescape(unquote(item['name'])).replace(u'\xa0', ' '), item['musicrid']) for item in response['list']])
        response = json.loads(get_response(quote(artist), i).text)["data"]
    ls.extend((html.unescape(unquote(item['name'])).replace(u'\xa0', ' '), item['musicrid']) for item in response['list'])
    with open(f'kuwo_{artist}.json', encoding='utf-8') as f:
        j = json.load(f)
    if new := set(ls) - set(tuple(x) for x in j):
        print(f"新曲目{len(new)}: {new}")
    if update:
        with open(f'kuwo_{artist}.json', 'w', encoding='utf-8') as f:
            json.dump(ls, f)


artists = ["Ampyx", "CHPTRS", "Vexento", "Dabin", "Lights & Motion", "Marcus Warner", "The Piano Guys",
           "Thomas Bergerson", "Tony Anderson"] # Jannik and Minecraft
for artist in artists:
    # with open(f"kuwo_{artist}.json", 'w', encoding='utf-8') as f:
    #     f.write("[]\n")
    check_an_artist(artist)