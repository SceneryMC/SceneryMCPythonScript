from n_image_downloader_temp import temp_get_image, base_url_pre, base_url_suf
import undetected_chromedriver as uc
from selenium import webdriver
from multiprocessing.dummy import Pool
import re
import os
import time


path = r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n'


def get_images(serial):
    url = f"https://nhentai.net/g/{serial}"
    driver.get(url)
    s = driver.page_source
    n = int(re.search(r'<span class="name">(\d+)</span></a></span></div><div class="tag-container field-name">', s).group(1))

    print(f'{url}开始下载！n = {n}')
    address_temp = rf"{path}\{serial}"
    if not os.path.exists(address_temp):
        os.mkdir(address_temp)

    driver.get(f"{url}/1")
    s = driver.page_source
    pattern = re.search(r'<img src="https://i(\d)\.nhentai\.net/galleries/(\d+)/\d+\.(jpg|png|gif)', s)
    server, inner_serial = pattern.group(1), pattern.group(2)
    folder = f"{base_url_pre}{server}{base_url_suf}/{inner_serial}"
    while len(dir_ls := os.listdir(address_temp)) != n:
        ls = {int(x.split('.')[0]) for x in dir_ls}
        ls_download = set(range(1, n+1)) - ls
        print(ls_download)

        p = Pool()
        for i in ls_download:
            p.apply_async(temp_get_image, args=(i, serial, folder, address_temp,))
        p.close()
        p.join()
    print(f'{url}下载完成！')


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--window-size=192,108")
    driver = uc.Chrome(options=options)
    driver.get(f"https://nhentai.net/g/400000")
    time.sleep(15)

    with open("n_site.txt", 'r') as f:
        content = [s.lstrip('#') for s in f.read().split()]
    for s in content:
        get_images(s)

    driver.close()
