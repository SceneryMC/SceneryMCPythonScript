import os
import json

from path_cross_platform import *
from pdf_page_and_annot_linker import command_template
from mm_filelist import filelist, bookxnote_root_windows

# 在IDE中执行python程序，编译器会自动把当前项目的根目录加入到包查找路径中，可以理解为加到PYTHONPATH下，所以直接执行是没有问题的
# 但是在cmd或者terminal控制台中直接使用python相关命令来执行程序，不会自动将当前项目加入到PYTHONPATH环境变量下，
# 如果涉及到import其他文件夹下的变量就会报类似ImportError: No module named xxx这样的错误。
#
# 解决方法是使用sys.path.append()命令把报警包的所在文件夹路径加入到PYTHONPATH

for file in filelist.values():
    with open(path_fit_platform(file[0]), 'r', encoding="utf-8") as f:
        content = f.read()
    content = content.replace(t1[not isLinux], t1[isLinux])
    content = content.replace(t2[not isLinux], t2[isLinux])
    with open(path_fit_platform(file[0]), 'w', encoding="utf-8") as f:
        f.write(content)


for root, _, files in os.walk(path_fit_platform(bookxnote_root_windows)):
    if os.path.dirname(root) == path_fit_platform(bookxnote_root_windows):
        with open(f"{root}/manifest.json", encoding='utf-8') as f:
            j = json.load(f)
        print(j)
        if platform_not_match(p := j['res'][0]['refpath']):
            j['res'][0]['refpath'] = func_dict[platform](p)
            with open(f"{root}/manifest.json", 'w', encoding='utf-8') as f:
                json.dump(j, f, ensure_ascii=False)
