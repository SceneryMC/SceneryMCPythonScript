import re
import os
import requests
import time

site = 'http://www.kebenzhan.com/'
prefix = '/d/file/renjiaoban/'
postfix = '.jpg'
address = r"G:\收藏\文档\！教材！\2001\语文"
name_dict = {"yuwenshangce": "语文上册", "yuwenxiace": "语文下册",
             "yinianji": "一年级", "ernianji": "二年级", "sannianji": "三年级", "sinianji": "四年级", "wunianji": "五年级",
             "liunianji": "六年级", "qinianji": "七年级", "banianji": "八年级", "jiunianji": "九年级"}


def download_textbook(url):
    r = requests.get(url)
    text = r.text
    images = [substr for substr in re.findall(rf"{prefix}([\w/]*)\{postfix}", text)]
    i = 1

    for image in images:
        print(image)

        while True:
            try:
                ri = requests.get(f"{site}{prefix}{image}{postfix}")
                break
            except requests.exceptions.ConnectionError:
                print("TOO FAST!")
                time.sleep(5)

        with open(rf'{address}\{file}\{i}{postfix}', 'wb') as f:
            f.write(ri.content)
        i += 1
    # time.sleep(1)


with open('n_site.txt') as f:
    for line in f:
        line = line.strip()
        url_split = line.split('/')
        file = f"{name_dict[url_split[-3]]}{name_dict[url_split[-2]]}"
        os.mkdir(rf"{address}\{file}")
        print(f"{line}开始下载！")
        download_textbook(line)
