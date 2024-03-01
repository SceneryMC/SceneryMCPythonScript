import os

from path_cross_platform import path_fit_platform

for root, dirs, files in os.walk('/mnt/F/存储/其它/!SD/'):
    for file in files:
        dst = os.path.join(root, file)
        if os.path.islink(dst):
            src = os.readlink(dst)
            os.remove(dst)
            os.link(src, dst)
            print(src, dst)
