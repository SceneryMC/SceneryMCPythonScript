import os
import shutil

current_path = r"C:\Users\SceneryMC\Downloads\Compressed\spritepacks-combined\gifts"
old_path = r"E:\时间的沉淀\游戏\DDLC\DDLC-1.1.1-pc\given_gifts"
dst_path = r"E:\时间的沉淀\游戏\DDLC\DDLC-1.1.1-pc\characters"
current_gifts = list(os.walk(current_path))[0][2]
old_gifts = list(os.walk(old_path))[0][2]
new_gifts = set(current_gifts) - set(old_gifts)
for gift in new_gifts:
    shutil.copy(rf"{current_path}\{gift}", dst_path)
    shutil.copy(rf"{current_path}\{gift}", old_path)
    print(f"{gift} added!")


# def get_gift_names(path):
#     gift_names = set()
#     no_gift_name_files = set()
#     for path, dir_list, file_list in os.walk(path):
#         for file in file_list:
#             with open(f"{path}\\{file}") as f:
#                 j = json.load(f)
#                 if "giftname" in j:
#                     gift_names.add(j['giftname'])
#                 else:
#                     no_gift_name_files.add(file)
#     return gift_names, no_gift_name_files
#
#
# gifts, missings = get_gift_names(r"C:\Users\SceneryMC\Downloads\Compressed\spritepacks-combined\mod_assets\monika\j")
# old_gifts, old_missings = get_gift_names(r"F:\Toolkit\Backup\DESKTOP-I0GMN8I\E\时间的沉淀\游戏\DDLC\DDLC-1.1.1-pc\game\mod_assets\monika\j")
# print(gifts - old_gifts)
# print(len(missings - old_missings))

