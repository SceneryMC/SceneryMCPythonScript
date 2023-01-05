from pdf_page_and_annot_linker import isLinux, address_in_platform, t1, generate_t2
from mm_filelist import filelist


for file in filelist.values():
    t2 = generate_t2(file[1])
    with open(address_in_platform(file[0]), 'r', encoding="utf-8") as f:
        content = f.read()
    content = content.replace(t1[not isLinux], t1[isLinux])
    content = content.replace(t2[not isLinux], t2[isLinux])
    with open(address_in_platform(file[0]), 'w', encoding="utf-8") as f:
        f.write(content)
