import os
from incremental_downloader_of_hubble_and_eso import eso_attributes, get_image_urls, get_total


def name_unify(s):
    s = s.lower()
    return s[:-3] if s.endswith("-en") else s


ls_local = []
ls_skipped = []
ls_all = []
ls_refetch = []
for root, folders, files in os.walk(r"G:\收藏\图片\ESO"):
    for file in files:
        file = file.split('.')[0]
        file = name_unify(file)
        ls_local.append(file)
with open("skipped_eso.txt") as f:
    for url in f:
        file = url.split('/')[-1][:-1].split('.')[0]
        file = name_unify(file)
        ls_skipped.append(file)
with open("processed_list_eso.txt") as f:
    for file in f:
        file = file[:-1]
        file = name_unify(file)
        ls_all.append(file)
with open("refetch_eso_image_list") as f:
    for file in f:
        file = file[:-1]
        file = name_unify(file)
        ls_refetch.append(file)


print("----------NUM----------")
set_local = set(ls_local)
print(len(ls_local), len(set_local))

set_skipped = set(ls_skipped)
print(len(ls_skipped), len(set_skipped))

set_local_and_skipped = set_local.union(set_skipped)
print(len(set_local_and_skipped))

set_processed = set(ls_all)
print(len(ls_all), len(set_processed))

set_refetch = set(ls_refetch)
print()

print("----------INTERSECT_LIST----------")
ans1, ans2 = set_local_and_skipped - set_processed, set_processed - set_local_and_skipped
ans1 = sorted(list(ans1))
ans2 = sorted(list(ans2))
print(len(ans1), ans1)
print(len(ans2), ans2)
print(len(set_local_and_skipped.intersection(set_processed)))

ans3, ans4 = set_processed - set_refetch, set_refetch - set_processed
ans3 = sorted(list(ans3))
ans4 = sorted(list(ans4))
print(len(ans3), ans3)
print(len(ans4), ans4)

ans5, ans6 = set_local_and_skipped - set_refetch, set_refetch - set_local_and_skipped
ans5 = sorted(list(ans5))
ans6 = sorted(list(ans6))
print(len(ans5), ans5)
print(len(ans6), ans6)

ans7, ans8 = set_processed - set_refetch, set_refetch - set_processed
ans7 = sorted(list(ans7))
ans8 = sorted(list(ans8))
print(len(ans7), ans7)
print(len(ans8), ans8)

print("----------REPEATS----------")
print("-----local-----")
ls_local.sort()
for i in range(len(ls_local)-2):
    if ls_local[i] == ls_local[i+1]:
        print(ls_local[i])
print("-----skipped-----")
ls_skipped.sort()
for i in range(len(ls_skipped)-2):
    if ls_skipped[i] == ls_skipped[i+1]:
        print(ls_skipped[i])
print("-----all-----")
ls_all.sort()
for i in range(len(ls_all)-2):
    if ls_all[i] == ls_all[i+1]:
        print(ls_all[i])


refetch = False
if refetch:
    image_per_page, total = get_total(f"{eso_attributes['basename']}/1/?sort=-release_date")
    print(image_per_page, total)
    images = []
    for i in range(1, total // image_per_page + (total % image_per_page != 0) + 1):
        images.extend(get_image_urls(f"{eso_attributes['basename']}/{i}/?sort=-release_date"))
        print(f"page {i} collected!")
    images = '\n'.join([s.split('/')[-1] for s in images])
    with open('refetch_eso_image_list', 'w') as f:
        f.write(images)
