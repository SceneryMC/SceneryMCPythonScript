import os


with open('eso_all_images_14814.txt') as f:
    all = [s.strip() for s in f.readlines()]
with open('eso_skipped.txt') as f:
    skipped = [s.strip()[s.rfind('/')+1:-4] for s in f.readlines()]
downloaded = set([s[:-4] for s in os.listdir(r"G:\收藏\图片\ESO")])

# all.sort(key=lambda x: x.lower())
# for i in range(len(all)-1):
#     if all[i].lower() == all[i+1].lower():
#         print(all[i], all[i+1])
# skipped.sort(key=lambda x: x.lower())
# for i in range(len(skipped)-1):
#     if skipped[i].lower() == skipped[i+1].lower():
#         print(skipped[i], skipped[i+1])

