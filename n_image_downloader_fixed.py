from n_image_downloader_temp import temp_get_image, base_url_pre, base_url_suf
import undetected_chromedriver as uc
from selenium import webdriver
from multiprocessing import Pool
import re
import os
import time


address = r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n'
sign = {'page_num_prefix': '<span class="name">',
        'page_num_suffix': '</span></a></span></div><div class="tag-container field-name">',
        'serial_prefix': "https://nhentai.net/g/", 'image': '<img src="'}


def get_images(serial):
    url = f"https://nhentai.net/g/{serial}"
    driver.get(url)
    s = driver.page_source
    b1 = re.search(r'<span class="name">\d+</span></a></span></div><div class="tag-container field-name">', s).group()
    n = int(re.findall(r"\d+", b1)[0])

    print(f'{url}开始下载！n = {n}')
    address_temp = rf"{address}\{serial}"
    if not os.path.exists(address_temp):
        os.mkdir(address_temp)

    driver.get(f"{url}/1")
    s = driver.page_source
    b2 = re.search(r'<img src="https://i\d\.nhentai\.net/galleries/\d+/\d+\.(jpg|png|gif)', s).group()
    server = re.findall(r"i\d", b2)[0][1]
    inner_serial = re.findall(r"galleries/\d+", b2)[0].split('/')[1]
    folder = f"{base_url_pre}{server}{base_url_suf}/{inner_serial}"
    while True:
        ls = {int(x[:x.find('.')]) for x in os.listdir(address_temp)}
        ls_download = set(range(1, n+1)) - ls
        print(ls_download)

        p = Pool()
        for i in ls_download:
            p.apply_async(temp_get_image, args=(i, serial, folder, address_temp,))
        p.close()
        p.join()

        if len(os.listdir(address_temp)) == n:
            break
    print(f'{url}下载完成！')


if __name__ == '__main__':
    options = webdriver.ChromeOptions()
    options.headless = False
    options.add_argument("--window-size=192,108")
    driver = uc.Chrome(options=options)
    driver.get(f"{sign['serial_prefix']}400000")
    time.sleep(10)

    with open("n_site.txt", 'r') as f:
        for line in f:
            line = line.strip().split()
            if line:
                get_images(line[0])

    driver.close()
