from multiprocessing import Pool
import requests
import urllib3
import time
import os
from n_image_downloader import headers, proxies, address

base_url_pre = "https://i"
base_url_suf = ".nhentai.net/galleries"
servers = [3, 5, 7]
fmts = ['jpg', 'png']


def temp_get_images(serial, n, inner_serial):
    urllib3.disable_warnings()
    address_temp = rf"{address}\{serial}"
    if not os.path.exists(address_temp):
        os.mkdir(address_temp)

    print(f'{serial}开始下载！n = {n}')
    for server in servers:
        for fmt in fmts:
            r = requests.get(f"{base_url_pre}{server}{base_url_suf}/{inner_serial}/1.{fmt}", verify=False,
                             headers=headers, proxies=proxies, stream=True)
            if int(r.headers['content-length']) > 1024:
                folder = f"{base_url_pre}{server}{base_url_suf}/{inner_serial}"
                break
    while True:
        ls = [int(x[:x.find('.')]) for x in os.listdir(address_temp)]
        ls_download = []
        for i in range(1, n + 1):
            if i not in ls:
                ls_download.append(i)
        print(ls_download)

        p = Pool()
        for i in ls_download:
            p.apply_async(temp_get_image, args=(i, serial, folder, address_temp,))
        p.close()
        p.join()

        if len(os.listdir(address_temp)) == n:
            break
    print(f'{serial}下载完成！')


def temp_get_image(i, serial, folder, address_temp):
    urllib3.disable_warnings()
    print(f"{serial}-{i}开始下载！")

    for fmt in fmts:
        r_sub = requests.get(f"{folder}/{i}.{fmt}", verify=False, headers=headers, proxies=proxies, stream=True)
        if int(r_sub.headers['content-length']) > 1024:
            while True:
                try:
                    r_sub = requests.get(f"{folder}/{i}.{fmt}", verify=False, headers=headers, proxies=proxies)
                    break
                except:
                    print(f"图片{i}出现一次下载错误！重试中……")
                    time.sleep(5)
            with open(rf"{address_temp}\{i}.{fmt}", 'wb') as f:
                f.write(r_sub.content)
                print(f"{i}完成！")
            break


if __name__ == '__main__':
    with open("n_site.txt", 'r') as f:
        for line in f:
            line = [int(x) for x in line.strip().split()]
            if len(line) == 3:
                temp_get_images(line[0], line[1], line[2])


# view-source:https://nhentai.net/g//1
