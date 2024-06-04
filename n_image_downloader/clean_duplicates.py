import numpy as np
import pickle
import cv2
import os
import re
from n_image_downloader.utils import get_all_exist, artist_path, get_all_works_of_artists, alias

# 思路是对的，但SIFT完全不能用
a = 32
d = get_all_exist(artist_path)
artists = get_all_works_of_artists()
database_path = "text_files/database.pickle"
with open(database_path, 'rb') as f:
    database = pickle.load(f)

type keypoints_storage = list[int]


def cv_imread(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)


def get_keypoints_of_a_work(work_path) -> keypoints_storage:
    result = []
    file_list = [file for file in os.listdir(work_path) if re.match(r"\d+\.(png|jpg)", file)]
    for image_name in sorted(file_list, key=lambda x: int(x[:x.index('.')])):
        try:
            img = cv_imread(os.path.join(work_path, image_name))
            img = cv2.resize(img, (a + 1, a))
        except:
            result.append(0)
            print(f"{image_name} of {work_path} ERROR!")
        else:
            hash_str = 0
            bit = 1
            # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
            for i in range(a):
                for j in range(a):
                    if img[i, j] > img[i, j + 1]:
                        hash_str |= bit
                    bit <<= 1
            # print(image_name, f"{hash_str:0{a**2}b}")
            result.append(hash_str)
    return result


def is_work_duplicate(new_path, new_artist,
                      keypoints_database=database, artist_database=artists,
                      new_id='', new_result=None) -> str:
    if new_result is None:
        new_result = get_keypoints_of_a_work(new_path)

    if (new_artist := alias.get(new_artist, new_artist)) not in artist_database:
        return ''
    for work_id in artist_database[new_artist]:
        if new_id == work_id:
            continue

        duplicate_count = 0
        for i in range(len(new_result)):
            for j in range(len(keypoints_database[work_id])):
                s = f"{new_result[i] ^ keypoints_database[work_id][j]:0{a ** 2}b}"
                if s.count("0") > a ** 2 * 0.9:
                    duplicate_count += 1
                    break
        denominator = min(len(new_result), len(keypoints_database[work_id]))
        print(work_id, duplicate_count, denominator)
        if denominator != 0 and duplicate_count / denominator > 0.3:
            return work_id
    return ''


def build_keypoints_database():
    result = {}
    for work_id, work_path in d.items():
        print(work_path, work_id)
        result[work_id] = get_keypoints_of_a_work(os.path.join(work_path, work_id))
    return result


def clean_duplicates_in_database(database):
    for artist, works in artists.items():
        if len(works) == 1:
            continue

        for work_id, work_path in works.items():
            # print(f"processing {work_id}...", end='\t')
            if (p := is_work_duplicate(os.path.join(work_path, work_id), artist, database, artists,
                                       work_id, database[work_id])) != '':
                print(f"{work_id} duplicates with {p}!")


if __name__ == '__main__':
    # database = build_keypoints_database()
    # with open(database_path, 'wb') as f:
    #     pickle.dump(database, f)
    # clean_duplicates_in_database(database)
    r = is_work_duplicate(r"C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n\500854",
                          "kakao",
                          database, artists)
    print(r)
