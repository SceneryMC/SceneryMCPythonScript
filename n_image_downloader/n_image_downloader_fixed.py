from n_image_downloader_temp import temp_get_image, base_url_pre, base_url_suf
import undetected_chromedriver as uc
from selenium import webdriver
from multiprocessing.dummy import Pool
import re
import os
import time
import json

global driver, d_last, d_all
tmp_path = r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n'
test_url = "https://nhentai.net/g/400000"
last_log = 'last_n_site.json'
all_log = 'all_n_site.json'
download_list_file = 'n_site.txt'


def get_basic_info(url):
    driver.get(url)
    src = driver.page_source

    artist = re.search(r'<span class="tags"><a href="/artist/([^/]+)/"', src)
    parodies = re.search('/parody/([^/]+)/', src)
    return {'artist': artist.group(1) if artist else None,
            'tags': re.findall(r'"/tag/([^/]+)/"', src),
            'characters': re.findall(r'"/character/([^/]+)/"', src),
            'parodies': parodies.group(1) if parodies else None,
            }, int(
                re.search(r'<span class="name">(\d+)</span></a></span></div><div class="tag-container field-name">',
                          src).group(
                    1)), "/language/chinese/" in src


def generate_url(work):
    return f"https://nhentai.net/g/{work}"


def visit_work(work, Chinese_only):
    url = generate_url(work)
    d, n, isChinese = get_basic_info(url)
    print(f'{url}: n = {n}')

    if not Chinese_only or isChinese:
        download_images(work, n)
        d_last[work] = d_all[work] = d
        save_log()

    print(f'{url}完成！')


def download_images(work, n):
    address_temp = rf"{tmp_path}\{work}"
    if not os.path.exists(address_temp):
        os.mkdir(address_temp)

    while True:
        try:
            driver.get(f"{generate_url(work)}/1")
            s = driver.page_source
            pattern = re.search(r'<img src="https://i(\d)\.nhentai\.net/galleries/(\d+)/\d+\.(jpg|png|gif)', s)
            server, inner_serial = pattern.group(1), pattern.group(2)
            break
        except:
            time.sleep(5)
            print("VPN DOWN!")
    folder = f"{base_url_pre}{server}{base_url_suf}/{inner_serial}"
    while len(dir_ls := os.listdir(address_temp)) != n:
        ls_download = set(range(1, n + 1)) - {int(x.split('.')[0]) for x in dir_ls}
        print(ls_download)

        p = Pool()
        for i in ls_download:
            p.apply_async(temp_get_image, args=(i, work, folder, address_temp,))
        p.close()
        p.join()


def save_log():
    with open(last_log, 'w') as f:
        json.dump(d_last, f, ensure_ascii=False, indent=True)
    with open(all_log, 'w') as f:
        json.dump(d_all, f, ensure_ascii=False, indent=True)


def init_driver():
    global driver
    options = webdriver.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.set_window_size(192, 168)
    driver.get(test_url)
    time.sleep(90)


def load_log():
    global d_last, d_all
    with open(last_log) as f:
        d_last = json.load(f)
    with open(all_log) as f:
        d_all = json.load(f)


def process_requests(allow_duplicate):
    with open(download_list_file) as f:
        content = re.findall("(\d{1,6})", f.read())
    for s in content:
        if s not in d_last and (allow_duplicate or s not in d_all):
            visit_work(s, True)


if __name__ == '__main__':
    init_driver()
    load_log()
    process_requests(False)

    driver.close()
