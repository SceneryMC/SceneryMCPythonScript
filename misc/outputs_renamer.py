import os
from path_Windows_to_Linux import *


for root, folders, files in os.walk(
        path_Windows_to_Linux(r"F:\存储\其它\outputs")):
    if not all([x[:-4].isdigit() for x in files]):
        print(root)
        for i in range(len(files)):
            os.rename(f"{root}/{files[i]}", f"{root}/000{i}.png")
        for i in range(len(files)):
            os.rename(f"{root}/000{i}.png", f"{root}/{i}.png")
