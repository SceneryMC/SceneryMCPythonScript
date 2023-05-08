from multiprocessing import Pool
import requests
import urllib3
import time
import os

base_url_pre = "https://i"
base_url_suf = ".nhentai.net/galleries"
servers = [3, 5, 7]
fmts = ['jpg', 'png', 'gif']

path = r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n'
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,"
              "application/signed-exchange;v=b3;q=0.9",
    # noqa
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "Dnt": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 Safari/537.36",
    # noqa
}


def temp_get_images(serial, n, inner_serial):
    urllib3.disable_warnings()
    address_temp = rf"{path}\{serial}"
    if not os.path.exists(address_temp):
        os.mkdir(address_temp)

    print(f'{serial}开始下载！n = {n}')
    for server in servers:
        for fmt in fmts:
            r = requests.get(f"{base_url_pre}{server}{base_url_suf}/{inner_serial}/1.{fmt}", verify=False,
                             headers=headers, stream=True)
            if int(r.headers['content-length']) > 1024:
                folder = f"{base_url_pre}{server}{base_url_suf}/{inner_serial}"
                break
    while len(dir_ls := os.listdir(address_temp)) != n:
        ls = [int(x[:x.find('.')]) for x in dir_ls]
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
    print(f'{serial}下载完成！')


def temp_get_image(i, serial, folder, address_temp):
    urllib3.disable_warnings()
    print(f"{serial}-{i}开始下载！")

    for fmt in fmts:
        r_sub = requests.get(f"{folder}/{i}.{fmt}", verify=False, headers=headers, stream=True)
        if int(r_sub.headers['content-length']) > 1024:
            while True:
                try:
                    r_sub = requests.get(f"{folder}/{i}.{fmt}", verify=False, headers=headers)
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
                temp_get_images(*line)


# view-source:https://nhentai.net/g//1
