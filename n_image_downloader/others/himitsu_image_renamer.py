import os

address = r"C:\Non-installed softwares\xeHentai-2.0.2.3-稳定版.exe\download\[haneruHimitsuひみつTokinohimitsu galleryDoujinshi ^-^][chinese][english]"
src = int(input())
inc = int(input())

files = os.listdir(address)
n = len(files)
for i in range(n, src - 1, -1):
    os.rename(rf"{address}\{i:03}.jpg", rf"{address}\{i + inc:03}.jpg")