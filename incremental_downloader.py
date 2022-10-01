import re
import time
import requests
from multiprocessing.dummy import Pool

hubble_attributes = {'folder': 'Hubble', 'name': 'hubble',
                     'source': 'https://esahubble.org/media/archives/images/original',
                     'suffix': "https://esahubble.org/images",
                     'frontpage': "https://esahubble.org/images/viewall/page/1/?sort=-release_date"}
eso_attributes = {'folder': 'ESO', 'name': 'eso',
                  'source': 'https://cdn.eso.org/images/original',
                  'suffix': "https://www.eso.org/public/images",
                  'frontpage': "https://www.eso.org/public/images/list/1/?sort=-release_date"}


def get_urls(url):
    html_text = requests.get(url).text
    url_text = re.search(r'var images.*?</script><div class="image-list image-list-\d+', html_text, re.DOTALL).group()
    total = int(re.search(r"Showing 1 to \d+ of (\d+)", html_text).group(1))

    ls = re.findall(rf"id: '(\w+)',", url_text)
    return ls, total


def download_image(image, suffix):
    print(f"downloading {image}.{suffix}...")

    r = requests.head(f"{attributes['source']}/{image}.{suffix}")
    image_size = int(r.headers['content-length'])
    if image_size > 100 * 1024 ** 2:
        print(f"TOO LARGE: SIZE = {image_size / 1024 ** 2} MB!")
        with open("skipped.txt", 'a') as f:
            f.write(f"{attributes['source']}/{image}.{suffix}\n")
        return

    with open(rf'G:\收藏\图片\{attributes["folder"]}\{image}.{suffix}', "wb") as f:
        pass
    start, end, step = 0, image_size, 8 * 1024 ** 2
    image_segment = [(start, min(start+step, end)-1) for start in range(0, end, step)]
    p = Pool()
    for i in image_segment:
        p.apply_async(download_image_thread, args=(image, suffix, i))
    p.close()
    p.join()


def download_image_thread(image, suffix, i):
    headers = {"range": f"bytes={i[0]}-{i[1]}"}
    print(headers)
    while True:
        try:
            r = requests.get(f"{attributes['source']}/{image}.{suffix}", headers=headers, stream=True)
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    with open(rf'G:\收藏\图片\{attributes["folder"]}\{image}.{suffix}', 'rb+') as f:
        f.seek(i[0])
        for chunk in r.iter_content(chunk_size=64 * 1024):
            if chunk:
                f.write(chunk)


def get_suffix(image):
    html_text = requests.get(f"{attributes['suffix']}/{image}").text
    suffix_index = html_text.find("Fullsize Original")
    return html_text[suffix_index - 5:suffix_index - 2]


if __name__ == '__main__':
    attributes = hubble_attributes

    with open(f'downloaded_{attributes["name"]}.txt') as f:
        downloaded = int(f.readline())
    images, total = get_urls(attributes['frontpage'])
    images = images[:total - downloaded]
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
