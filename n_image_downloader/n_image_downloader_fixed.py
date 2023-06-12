from n_image_downloader_temp import temp_get_image, base_url_pre, base_url_suf
import undetected_chromedriver as uc
from selenium import webdriver
from multiprocessing.dummy import Pool
import re
import os
import time
import json

path = r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n'


def get_basic_info(url):
    driver.get(url)
    s = driver.page_source

    artist = re.search(r'<span class="tags"><a href="/artist/([^/]+)/"', s)
    parodies = re.search('/parody/([^/]+)/', s)
    return {'artist': artist.group(1) if artist else None,
            'tags': re.findall(r'"/tag/([^/]+)/"', s),
            'characters': re.findall(r'"/character/([^/]+)/"', s),
            'parodies': parodies.group(1) if parodies else None,
            }, int(
                re.search(r'<span class="name">(\d+)</span></a></span></div><div class="tag-container field-name">',
                          s).group(
                    1))


def get_images(serial, download):
    url = f"https://nhentai.net/g/{serial}"
    d, n = get_basic_info(url)

    print(f'{url}开始下载！n = {n}')
    if download:
        address_temp = rf"{path}\{serial}"
        if not os.path.exists(address_temp):
            os.mkdir(address_temp)

        while True:
            try:
                driver.get(f"{url}/1")
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
                p.apply_async(temp_get_image, args=(i, serial, folder, address_temp,))
            p.close()
            p.join()

    d_last[serial] = d_all[serial] = d
    with open("last_n_site.json", 'w') as f:
        json.dump(d_last, f, ensure_ascii=False, indent=True)
    with open('all_n_site.json', 'w') as f:
        json.dump(d_all, f, ensure_ascii=False, indent=True)
    print(f'{url}下载完成！')


if __name__ == '__main__':
    download = input("是否下载？") != "False"
    options = webdriver.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.set_window_size(192, 168)
    driver.get(f"https://nhentai.net/g/400000")
    time.sleep(30)

    with open("last_n_site.json") as f:
        d_last = json.load(f)
    with open('all_n_site.json') as f:
        d_all = json.load(f)
    with open("n_site.txt") as f:
        content = re.findall("(\d{1,6})", f.read())
    for s in content:
        if s not in d_last:
            get_images(s, download)

    driver.close()
