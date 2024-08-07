import json
import os
import re
import time
import undetected_chromedriver as uc
from selenium import webdriver
from collections import defaultdict
from n_image_downloader.config import artist_path
from n_image_downloader.utils import alias, all_log, generate_test_url, download_list_file, \
    get_all_works_of_artists

global local_last_work, driver
artist_new_work = 'text_files/n_new_work.json'
works_per_page = 25


def generate_url(artist, page):
    return f"https://nhentai.net/artist/{artist}/?page={page}"


def visit_artist(artist, last_work):
    page = 1
    works = []
    inf = max(last_work, local_last_work[artist])
    tmp_works = list(range(works_per_page))
    while len(tmp_works) == works_per_page:
        while True:
            driver.get(generate_url(artist, page))
            src = driver.page_source
            if ((ls := re.findall(r'<a href="/g/(\d+)/" class="cover"', src))
                    or '<h3>No results, sorry.</h3>' in src):
                break
            print(src)
            time.sleep(30)

        tmp_works = [int(w) for w in ls if int(w) > inf]
        works.extend(tmp_works)
        page += 1

        time.sleep(0.5)
    return works


def visit_artists(last_work, load_func):
    global local_last_work
    local_last_work = load_func()

    new_works = defaultdict(list)
    for artist in local_last_work.keys():
        new_work = visit_artist(artist, last_work)
        new_works[alias.get(artist, artist)].extend(new_work)
        print(f"{artist} done! {new_work}")

    with open(artist_new_work, 'w') as f:
        json.dump(new_works, f, ensure_ascii=False, indent=True)


def load_local():
    d = defaultdict(lambda: 0)
    selected = default_artist()
    with open(all_log, encoding='utf-8') as f:
        j = json.load(f)
    for work, info in j.items():
        if 'artist' in info and (artist := info['artist']) in selected and int(work) > d[artist]:
            d[artist] = int(work)
    return d


def default_artist():
    s = set()
    s |= set(os.listdir(rf"{artist_path}\4"))
    s |= set(os.listdir(rf"{artist_path}\5"))
    s |= set(os.listdir(rf"{artist_path}\6"))
    s |= set(alias.keys())

    return s


def load_specified(ignore_existed=True):
    with open(download_list_file) as f:
        d = {s: 0 for s in re.findall(r'https://nhentai\.net/artist/([^/]+)/', f.read())}
    if ignore_existed:
        ignored = set(d.keys()) & set(get_all_works_of_artists().keys())
        for artist in ignored:
            del d[artist]
            print(f"已存在，跳过：{artist}")
    return d


def init_driver():
    global driver
    options = webdriver.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.set_window_size(192, 168)
    driver.get(generate_test_url())
    time.sleep(30)


if __name__ == '__main__':
    cmd_to_func = {"a": load_local, "s": load_specified}

    last_work = int(input("最近作品？"))
    if last_work == -1:
        with open(all_log) as f:
            m = json.load(f)
            last_work = max(int(x) for x in m.keys())
    target = input("全部a/指定s？")
    print(f"last_work = {last_work}")

    init_driver()
    visit_artists(last_work, cmd_to_func[target])
