import os

address = r"D:\截图\DDLC"

files = os.walk(address)
for t in files:
    for file in t[2]:
        temp_address = t[0]
        # print(rf"{temp_address}\{file}")
        y, m, d, hns = file[4:8], file[8:10], file[10:12], file[12:18]
        os.rename(rf"{temp_address}\{file}", rf"{temp_address}\{y}-{m}-{d}_{hns}.png")
