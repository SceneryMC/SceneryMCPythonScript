import os


ls_local = []
ls_skipped = []
ls_all = []
for root, folders, files in os.walk(r"G:\收藏\图片\ESO"):
    for file in files:
        file = file.split('.')[0].lower()
        # file = file.split('-')[0]
        ls_local.append(file)
with open("skipped_eso.txt") as f:
    for url in f:
        file = url.split('/')[-1][:-1].split('.')[0].lower()
        # file = file.split('-')[0]
        ls_skipped.append(file)
with open("downloaded_list_eso.txt") as f:
    for file in f:
        file = file[:-1].lower()
        # file = file.split('-')[0]
        ls_all.append(file)

set_local = set(ls_local)
print(len(set_local))
set_skipped = set(ls_skipped)
print(len(set_skipped))
set_local_and_skipped = set_local.union(set_skipped)
print(len(set_local_and_skipped))
set_all = set(ls_all)
print(len(set_all))
ans1, ans2 = set_local_and_skipped - set_all, set_all - set_local_and_skipped

ans1 = sorted(list(ans1))
ans2 = sorted(list(ans2))
print(len(ans1), ans1)
print(len(ans2), ans2)
print(len(set_local_and_skipped.intersection(set_all)))

ls_all.sort()
for i in range(len(ls_all)-2):
    if ls_all[i] == ls_all[i+1]:
        print(ls_all[i])
