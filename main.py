import os
import shutil

address = r"G:\收藏\图片\ESO\others"
folders = ["_", "alma", "dsc", "ehpa", "img", "max", "uhd", "vista", "vlt"]
filelist = os.listdir(address)
print(filelist)
for t in folders:
    filelist.remove(t)
for s in os.listdir(address):
    for t in folders:
        if s[:len(t)] == t:
            shutil.move(rf"{address}\{s}", rf"{address}\{t}")
