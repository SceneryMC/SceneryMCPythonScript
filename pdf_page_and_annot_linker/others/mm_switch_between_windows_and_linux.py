import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_page_and_annot_linker import isLinux, address_in_platform, t1, generate_t2
from mm_filelist import filelist

# 在IDE中执行python程序，编译器会自动把当前项目的根目录加入到包查找路径中，可以理解为加到PYTHONPATH下，所以直接执行是没有问题的
# 但是在cmd或者terminal控制台中直接使用python相关命令来执行程序，不会自动将当前项目加入到PYTHONPATH环境变量下，
# 如果涉及到import其他文件夹下的变量就会报类似ImportError: No module named xxx这样的错误。
#
# 解决方法是使用sys.path.append()命令把报警包的所在文件夹路径加入到PYTHONPATH


for file in filelist.values():
    t2 = generate_t2(file[1])
    with open(address_in_platform(file[0]), 'r', encoding="utf-8") as f:
        content = f.read()
    content = content.replace(t1[not isLinux], t1[isLinux])
    content = content.replace(t2[not isLinux], t2[isLinux])
    with open(address_in_platform(file[0]), 'w', encoding="utf-8") as f:
        f.write(content)
