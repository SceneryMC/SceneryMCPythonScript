from maintain_artist import get_all_exist, artist_path
import numpy as np
import pickle
import cv2
import os


# 思路是对的，但SIFT完全不能用
sift = cv2.SIFT_create()
d = get_all_exist(r'F:\存储\其它\SYNC\ARTIST\6\key')


def cv_imread(path):
    return cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)

def get_all_works_of_authors():
    result = {}
    for rank in ["4", "5", "6"]:
        for author in os.listdir(os.path.join(artist_path, rank)):
            result[author] = get_all_exist(os.path.join(artist_path, rank, author))
    return result


def get_keypoints_of_a_work(work_path):
    result = []
    for image_name in sorted(os.listdir(work_path), key=lambda x: int(x[:x.index('.')])):
        print(image_name)
        img = cv_imread(os.path.join(work_path, image_name))
        kp, des = sift.detectAndCompute(img, None)
        result.append(des)
    return result


def is_work_duplicate(new_work, new_author, keypoints_database):
    pass


def build_keypoints_database():
    result = {}
    for work_id, work_path in d.items():
        print(work_path, work_id)
        result[work_id] = get_keypoints_of_a_work(os.path.join(work_path, work_id))
    return result


if __name__ == '__main__':
    database = build_keypoints_database()
    with open('database.pickle', 'wb') as f:
        pickle.dump(database, f)