from n_image_downloader_temp import temp_get_image, base_url_pre, base_url_suf
from n_image_downloader import address, sign
import undetected_chromedriver as uc
from selenium import webdriver
from multiprocessing import Pool
import re
import os
import time


def get_images(serial):
    url = f"{sign['serial_prefix']}{serial}"
    driver.get(url)
    s = driver.page_source
    b = re.search(rf'{sign["page_num_prefix"]}\d*{sign["page_num_suffix"]}', s)
    n = int(s[b.start() + len(sign['page_num_prefix']): b.end() - len(sign['page_num_suffix'])])

    print(f'{url}开始下载！n = {n}')
    address_temp = rf"{address}\{serial}"
    if not os.path.exists(address_temp):
        os.mkdir(address_temp)

    driver.get(f"{url}/1")
    s = driver.page_source
    b_temp = re.search(rf'<a href="/g/\d+/\d*/?">{sign["image"]}', s)
    b = b_temp.start() + s[b_temp.start():].find(sign['image']) + len(sign['image'])
    e = b + s[b:].find('"')
    sample_address = s[b:e].split('/')
    server, inner_serial = sample_address[2][1], sample_address[-2]
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
