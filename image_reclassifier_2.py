import os
import shutil

address = r"G:\收藏\图片\Hubble"
folders = ["heic", "potw", "opo", "sci", "ann", "others"]
images = os.listdir(address)
for folder in folders:
    images.remove(folder)
for image in images:
    dst_folder = folders[-1]
    for folder in folders[:-1]:
        if image[:len(folder)] == folder:
            dst_folder = folder
            break
    shutil.move(rf"{address}\{image}", rf"{address}\{dst_folder}\{image}")
