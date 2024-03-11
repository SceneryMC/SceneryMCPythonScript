from maintain_artist import get_all_exist, artist_path, get_all_works_of_authors
import numpy as np
import pickle
import cv2
import os
import array
import re


# 思路是对的，但SIFT完全不能用
d = get_all_exist(artist_path)
authors = get_all_works_of_authors()


def cv_imread(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)


def get_keypoints_of_a_work(work_path):
    result = array.array("Q")
    file_list = [file for file in os.listdir(work_path) if re.match(r"\d+\.(png|jpg)", file)]
    for image_name in sorted(file_list, key=lambda x: int(x[:x.index('.')])):
        try:
            img = cv_imread(os.path.join(work_path, image_name))
            img = cv2.resize(img, (9, 8))
        except:
            result.append(0)
            print(f"{image_name} of {work_path} ERROR!")
        else:
            hash_str = 0
            bit = 0
            # 每行前一个像素大于后一个像素为1，相反为0，生成哈希
            for i in range(8):
                for j in range(8):
                    hash_str |= (int(img[i, j] > img[i, j + 1]) << bit)
                    bit += 1
            # print(image_name, f"{hash_str:064b}")
            result.append(hash_str)
    return result


def is_work_duplicate(new_path, new_author, keypoints_database, new_id=-1, new_result=None):
    if new_result is None:
        new_result = get_keypoints_of_a_work(new_path)

    for work_id in authors[new_author]:
        if new_id == work_id:
            continue

        duplicate_count = 0
        for i in range(len(new_result)):
            for j in range(len(keypoints_database[work_id])):
                s = f"{new_result[i] ^ keypoints_database[work_id][j]:064b}"
                if s.count("0") > 60:
                    duplicate_count += 1
        print(work_id, duplicate_count, end=' ')
        denominator = min(len(new_result), len(keypoints_database[work_id]))
        if denominator != 0 and duplicate_count / denominator > 0.9:
            print(f"duplicate with {work_id}!")
            return work_id
    return -1


def build_keypoints_database():
    result = {}
    for work_id, work_path in d.items():
        print(work_path, work_id)
        result[work_id] = get_keypoints_of_a_work(os.path.join(work_path, work_id))
    return result


def clean_duplicates_in_database(database):
    for author, works in authors.items():
        if len(works) == 1:
            continue

        for work_id, work_path in works.items():
            print(f"processing {work_id}...", end='\t')
            if (p := is_work_duplicate(os.path.join(work_path, work_id), author, database, work_id, database[work_id])) != -1:
                with open('text_files/duplicates.txt', 'a') as f:
                    f.write(f"{work_id} duplicate with {p}!\n")
            else:
                print("unique!")


if __name__ == '__main__':
    # database = build_keypoints_database()
    # with open('database.pickle', 'wb') as f:
    #     pickle.dump(database, f)
    with open("database.pickle", 'rb') as f:
        database = pickle.load(f)
    clean_duplicates_in_database(database)
    # r = is_work_duplicate(r"C:\Users\SceneryMC\Downloads\图片助手(ImageAssistant)_批量图片下载器\n\500156",
    #                   "kyockcho",
    #                   database)
    # print(r)
