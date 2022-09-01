import urllib.request
from pdf_page_and_annot_linker import filelist, isLinux, address_in_platform, t1


for file in filelist:
    with open(address_in_platform(file[0]), 'r') as f:
        content = f.read()
    content = content.replace(t1[not isLinux], t1[isLinux])
    t2 = (urllib.request.quote(f'=OpenActions" "{address_in_platform(file[1], False)}"'), f' {address_in_platform(file[1], True)}')
    content = content.replace(t2[not isLinux], t2[isLinux])
    with open(address_in_platform(file[0]), 'w') as f:
        f.write(content)
# with open("/mnt/E/学习资料/计算机/参考书/可能会读的书/算法/算法导论/整理/CLRS.mm", 'r') as f:
#     content_original = f.read()
# print(content_original == content)

