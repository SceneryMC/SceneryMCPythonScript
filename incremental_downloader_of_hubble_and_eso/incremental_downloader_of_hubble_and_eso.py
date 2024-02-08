import re
import time
import requests
from multiprocessing.dummy import Pool
from path_cross_platform import *

hubble_attributes = {'folder': 'Hubble', 'name': 'hubble',
                     'source': 'https://esahubble.org/media/archives/images/original',
                     'suffix': "https://esahubble.org/images",
                     'basename': "https://esahubble.org/images/page"}
eso_attributes = {'folder': 'ESO', 'name': 'eso',
                  'source': 'https://www.eso.org/public/archives/images/original',
                  'suffix': "https://www.eso.org/public/images",
                  'basename': "https://www.eso.org/public/images/list"}
attribute_map = {"eso": eso_attributes, "hubble": hubble_attributes}


def get_image_urls(url):
    while True:
        try:
            html_text = requests.get(url).text
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    url_text = re.search(r'var images.*?</script><div class="image-list image-list-\d+', html_text, re.DOTALL).group()

    ls = re.findall(rf"id: '(.*?)',", url_text)
    return ls


def get_total(url):
    while True:
        try:
            html_text = requests.get(url).text
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    result = re.search(r"Showing 1 to (\d+) of (\d+)", html_text)
    return int(result.group(1)), int(result.group(2))


def download_image(image, suffix):
    print(f"downloading {image}.{suffix}...")

    while True:
        try:
            r = requests.head(f"{attributes['source']}/{image}.{suffix}")
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    image_size = int(r.headers['content-length'])
    if image_size > 96 * 1024 ** 2:
        print(f"TOO LARGE: SIZE = {image_size / 1024 ** 2} MB!")
        with open(f"results/skipped_{attributes['name']}.txt", 'a') as f:
            f.write(f"{attributes['source']}/{image}.{suffix}\n")
        return False

    with open(path_fit_platform(rf'G:\收藏\图片\{attributes["folder"]}\{image}.{suffix}'), "wb") as f:
        pass
    start, end, step = 0, image_size, 8 * 1024 ** 2
    image_segment = [(start, min(start+step, end)-1) for start in range(0, end, step)]
    p = Pool()
    for segment in image_segment:
        p.apply_async(download_image_thread, args=(image, suffix, segment))
    p.close()
    p.join()
    return True


def download_image_thread(image, suffix, segment):
    headers = {"range": f"bytes={segment[0]}-{segment[1]}"}
    print(headers)
    while True:
        try:
            r = requests.get(f"{attributes['source']}/{image}.{suffix}", headers=headers, stream=True)
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    with open(path_fit_platform(rf'G:\收藏\图片\{attributes["folder"]}\{image}.{suffix}'), 'rb+') as f:
        f.seek(segment[0])
        for chunk in r.iter_content(chunk_size=64 * 1024):
            if chunk:
                f.write(chunk)


def get_suffix(image):
    while True:
        try:
            html_text = requests.get(f"{attributes['suffix']}/{image}").text
            break
        except requests.exceptions.ConnectionError:
            print("TOO FAST!")
            time.sleep(5)
    suffix_index = html_text.find("Fullsize Original")
    return html_text[suffix_index - 5:suffix_index - 2]


def get_download_list(downloaded):
    image_per_page, total = get_total(f"{attributes['basename']}/1/?sort=-release_date")
    print(image_per_page, total)
    will_download = total - downloaded
    images = []
    for i in range(1, will_download // image_per_page + (will_download % image_per_page != 0) + 1):
        images.extend(get_image_urls(f"{attributes['basename']}/{i}/?sort=-release_date"))
        print(f"page {i} collected!")
    return images[will_download-1::-1]


if __name__ == '__main__':
    attributes = attribute_map[input("网站：")]
    with open(f'results/processed_amount_{attributes["name"]}.txt') as f:
        downloaded = int(f.readline())

    images = get_download_list(downloaded)
    for i in range(len(images)):
        if download_image(images[i], get_suffix(images[i])):
            print(f"{images[i]} downloaded!")
        with open(f"results/processed_list_{attributes['name']}.txt", 'a') as f:
            f.write(f"{images[i]}\n")
        with open(f'results/processed_amount_{attributes["name"]}.txt', 'w') as f:
            f.write(str(downloaded + i + 1))
