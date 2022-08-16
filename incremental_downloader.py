import re
import time
import requests

hubble_attributes = {'folder': 'Hubble', 'name': 'hubble', 'text_begin': "var images",
                     'text_end': '</script><div class="image-list image-list-150"></div>',
                     'total': "Showing 1 to 250 of ", 'image_identifier_begin': "id: '",
                     'image_identifier_end': "',",
                     'source': 'https://esahubble.org/media/archives/images/original',
                     'suffix': "https://esahubble.org/images", 'digit': 6,
                     'frontpage': "https://esahubble.org/images/viewall/page/1/?sort=-release_date"}
eso_attributes = {'folder': 'ESO', 'name': 'eso', 'text_begin': "var images",
                  'text_end': '</script><div class="image-list image-list-300"></div>',
                  'total': "Showing 1 to 50 of ", 'image_identifier_begin': "id: '",
                  'image_identifier_end': "',",
                  'source': 'https://cdn.eso.org/images/original',
                  'suffix': "https://www.eso.org/public/images", 'digit': 6,
                  'frontpage': "https://www.eso.org/public/images/?&sort=-release_date"}
target_site = input()
if target_site == 'hubble':
    attributes = hubble_attributes
elif target_site == 'eso':
    attributes = eso_attributes


def get_urls(url):
    html_text = requests.get(url).text
    s = html_text.find(attributes['text_begin'])
    e = html_text.find(attributes['text_end'])
    total_index = html_text.find(attributes['total'])
    url_text = html_text[s:e]

    ls = [substr for substr in re.findall(rf"{attributes['image_identifier_begin']}(\w*){attributes['image_identifier_end']}", url_text)]
    return ls, int(html_text[total_index + len(attributes['total']):total_index + len(attributes['total']) +
                                                                    attributes['digit']])


def download_image(image, suffix):
    print(f"downloading {image}.{suffix}...")

    r = requests.get(f"{attributes['source']}/{image}.{suffix}", stream=True)
    image_size = int(r.headers['content-length']) / 1024 ** 2
    if image_size > 100:
        print(f"TOO LARGE: SIZE = {image_size} MB!")
        with open("skipped.txt", 'a') as f:
            f.write(f"{attributes['source']}/{image}.{suffix}\n")
        return

    while True:
        try:
            r = requests.get(f"{attributes['source']}/{image}.{suffix}")
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    with open(rf'G:\收藏\图片\{attributes["folder"]}\{image}.{suffix}', 'wb') as f:
        f.write(r.content)


def get_suffix(image):
    html_text = requests.get(f"{attributes['suffix']}/{image}").text
    suffix_index = html_text.find("Fullsize Original")
    return html_text[suffix_index - 5:suffix_index - 2]


with open(f'downloaded_{attributes["name"]}.txt') as f:
    downloaded = int(f.readline())
images, total = get_urls(attributes['frontpage'])
images = images[:total-downloaded]
images.reverse()
i = 0
for image in images:
    suffix = get_suffix(image)
    download_image(image, suffix)
    print(f"{image} downloaded!")
    i += 1
    with open(f'downloaded_{attributes["name"]}.txt', 'w') as f:
        f.write(str(downloaded + i))


# import requests
# import re
# import os

# attributes = {'folder': 'Hubble', 'name': 'hubble', 'text_begin': "var images",
#                      'text_end': '</script><div class="image-list image-list-150"></div>',
#                      'total': "Showing 1 to 250 of ", 'image_identifier_begin': "url: '/images/",
#                      'image_identifier_end': "/",
#                      'source': 'https://esahubble.org/media/archives/images/original',
#                      'suffix': "https://esahubble.org/images", 'digit': 6,
#                      'frontpage': "https://esahubble.org/images/viewall/page/1/?sort=-release_date"}
#
#
# def get_urls(url):
#     print(f"{url}开始抓取！")
#     html_text = requests.get(url).text
#     s = html_text.find(attributes['text_begin'])
#     e = html_text.find(attributes['text_end'])
#     url_text = html_text[s:e]
#
#     ls = []
#     ls_indexes = [substr.start() for substr in re.finditer(attributes['image_identifier_begin'], url_text)]
#     for ls_index in ls_indexes:
#         end = url_text[ls_index + len(attributes['image_identifier_begin']):].find(attributes['image_identifier_end']) \
#               + ls_index + len(attributes['image_identifier_begin'])
#         ls.append(url_text[ls_index + len(attributes['image_identifier_begin']):end])
#
#     return ls
#
#
# n = 102
# result = []
# for i in range(1, n+1):
#     result.extend(get_urls(f"https://esahubble.org/images/viewall/page/{i}/?sort=-release_date"))
# with open('output.txt', 'a') as f:
#     for image in result:
#         f.write(f"{image}\n")

# file = list(os.walk(r"G:\收藏\图片\Hubble"))
# local_file_no_suffix = []
# for i in range(1,7):
#     for image in file[i][2]:
#         local_file_no_suffix.append(image.split('.')[0])
# with open('output.txt') as f:
#     web_file_no_suffix = [x.strip() for x in f.readlines()]
# web_file_no_suffix.sort()
# local_file_no_suffix.sort()
# len_web = len(web_file_no_suffix)
# len_local = len(local_file_no_suffix)
# print(len_web, len_local)
# i = j = 0
# while i < len_local and j < len_web:
#     if local_file_no_suffix[i] == web_file_no_suffix[j]:
#         i += 1
#     else:
#         print(web_file_no_suffix[j])
#     j += 1
