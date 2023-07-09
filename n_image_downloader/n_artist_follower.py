import json
import os
import re
import time
import undetected_chromedriver as uc
from selenium import webdriver
from maintain_artist import artist_alias, artist_path
from n_image_downloader_fixed import all_log, test_url
from collections import defaultdict

global local_last_work, driver
artist_new_work = 'n_new_work.json'
works_per_page = 25


def generate_url(artist, page):
    return f"https://nhentai.net/artist/{artist}/?page={page}"


def visit_artist(artist, last_work):
    page = 1
    works = []
    inf = max(last_work, local_last_work[artist])
    tmp_works = list(range(works_per_page))
    while len(tmp_works) == works_per_page:
        driver.get(generate_url(artist, page))
        src = driver.page_source

        tmp_works = [int(w) for w in re.findall(r'<a href="/g/(\d+)/" class="cover"', src) if int(w) > inf]
        works.extend(tmp_works)
        page += 1

        time.sleep(0.5)
    return works


def process_artist(last_work):
    global local_last_work
    local_last_work = load_num()
    with open(artist_alias) as f:
        alias = json.load(f)

    new_works = defaultdict(list)
    for artist in local_last_work.keys():
        new_works[alias.get(artist, artist)].extend(visit_artist(artist, last_work))
        print(f"{artist} done!")

    with open(artist_new_work, 'w') as f:
        json.dump(new_works, f, ensure_ascii=False, indent=True)


def load_num():
    d = defaultdict(lambda :0)
    selected = selected_artist()
    with open(all_log, encoding='utf-8') as f:
        j = json.load(f)
    for work, info in j.items():
        if 'artist' in info and (artist := info['artist']) in selected and int(work) > d[artist]:
            d[artist] = int(work)
    return d


def selected_artist():
    s = set()
    s = s.union(set(os.listdir(rf"{artist_path}\4")))
    s = s.union(set(os.listdir(rf"{artist_path}\5")))
    s = s.union(set(os.listdir(rf"{artist_path}\6")))
    with open(artist_alias) as f:
        alias = json.load(f)
    s = s.union(set(alias.keys()))

    return s


def init_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.set_window_size(192, 168)
    driver.get(test_url)
    time.sleep(30)


if __name__ == '__main__':
    last_work = int(input("最近作品？"))
    init_driver()
    process_artist(last_work)
