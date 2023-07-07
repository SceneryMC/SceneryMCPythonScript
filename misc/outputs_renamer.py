import os
from path_cross_platform import path_fit_platform


outputs_path = path_fit_platform(r"F:\存储\其它\outputs")


def rename(src, dst, num_renamed=0):
    dst_name = f"{dst}.png"
    num_renamed += 1

    if src == dst_name:
        files.remove(src)
        return num_renamed
    if dst_name in all_files:
        num_renamed += rename(dst_name, dst + 1)
    os.rename(f"{root}{os.sep}{src}", f"{root}{os.sep}{dst}.png")
    files.remove(src)
    all_files.remove(src)
    all_files.append(dst_name)
    return num_renamed


for root, folders, files in os.walk(outputs_path):
    if not all([x[:-4].isdigit() for x in files]):
        len_before = len(files)
        print(root)

        renamed_index = 0
        all_files = files[:]
        while files:
            renamed_index += rename(files[0], renamed_index)

        # for i in range(len(files)):
        #     os.rename(f"{root}/{files[i]}", f"{root}/000{i}.png")
        # for i in range(len(files)):
        #     os.rename(f"{root}/000{i}.png", f"{root}/{i}.png")
        assert len(os.listdir(root)) == len_before
