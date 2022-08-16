# import requests
# import urllib3
# from multiprocessing import Pool
# import re
# import os
# import time
#
address = r'C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n'
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
proxies = {'http': 'http://127.0.0.1:41091', 'https': 'http://127.0.0.1:41091'}
sign = {'page_num_prefix': '<span class="name">',
        'page_num_suffix': '</span></a></span></div><div class="tag-container '
                           'field-name">',
        'serial_prefix': "https://nhentai.net/g/", 'image': '<img src="'}
#
#
# def get_images(serial):
#     urllib3.disable_warnings()
#     url = f"{sign['serial_prefix']}{line}"
#     r = requests.get(url, verify=False, headers=headers, proxies=proxies)
#     s = r.text
#     b = re.search(rf'{sign["page_num_prefix"]}\d*{sign["page_num_suffix"]}', s)
#     n = int(s[b.start() + len(sign['page_num_prefix']): b.end() - len(sign['page_num_suffix'])])
#
#     print(f'{url}开始下载！n = {n}')
#     address_temp = rf"{address}\{serial}"
#     if not os.path.exists(address_temp):
#         os.mkdir(address_temp)
#
#     while True:
#         ls = [int(x[:x.find('.')]) for x in os.listdir(address_temp)]
#         ls_download = []
#         for i in range(1, n + 1):
#             if i not in ls:
#                 ls_download.append(i)
#         print(ls_download)
#
#         p = Pool()
#         for i in ls_download:
#             p.apply_async(get_image, args=(i, serial, url, address_temp,))
#         p.close()
#         p.join()
#
#         if len(os.listdir(address_temp)) == n:
#             break
#     print(f'{url}下载完成！')
#
#
# def get_image(i, serial, url, address_temp):
#     urllib3.disable_warnings()
#     print(f"{serial}-{i}开始下载！")
#
#     while True:
#         try:
#             r_sub = requests.get(f"{url}/{i}/", verify=False, headers=headers, proxies=proxies)
#             break
#         except:
#             print(f"{serial}：图片{i}出现一次下载错误！重试中……")
#             time.sleep(5)
#     s = r_sub.text
#
#     b_temp = re.search(r'<a href="/g/\d+/\d*/?"><img src="', s)
#     b = b_temp.start() + s[b_temp.start():].find(sign['image']) + len(sign['image'])
#     e = b + s[b:].find('"')
#     f = b + s[b:e].rfind('.')
#
#     while True:
#         try:
#             r_sub = requests.get(s[b:e], verify=False, headers=headers, proxies=proxies)
#             break
#         except:
#             print(f"{serial}：图片{i}出现一次下载错误！重试中……")
#             time.sleep(5)
#     with open(rf"{address_temp}\{i}.{s[f + 1:e]}", 'wb') as f:
#         f.write(r_sub.content)
#         print(f"{serial}-{i}完成！")
#
#
# if __name__ == '__main__':
#     with open("n_site.txt", 'r') as f:
#         for line in f:
#             line = line.strip().split()
#             if line:
#                 get_images(line[0])
