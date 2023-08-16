import json
import re
import yaml
from path_cross_platform import *
from pdf_page_and_annot_linker import generate_command

# 在IDE中执行python程序，编译器会自动把当前项目的根目录加入到包查找路径中，可以理解为加到PYTHONPATH下，所以直接执行是没有问题的
# 但是在cmd或者terminal控制台中直接使用python相关命令来执行程序，不会自动将当前项目加入到PYTHONPATH环境变量下，
# 如果涉及到import其他文件夹下的变量就会报类似ImportError: No module named xxx这样的错误。
# 解决方法是使用sys.path.append()命令把报警包的所在文件夹路径加入到PYTHONPATH

global pdf_path
with open('text_files/config.yaml', encoding='utf-8') as f:
    config = yaml.full_load(f)
with open('text_files/filelist.yaml', encoding='utf-8') as f:
    filelist = yaml.full_load(f)
    print(filelist)


def switch_platform(match):
    page_num = match.group(1)
    command = generate_command(pdf_path, page_num, platform)
    return command


other_platform = 'Linux' if platform == 'Windows' else 'Windows'
for file in filelist.values():
    mm_path, pdf_path = path_fit_platform(file[0]), path_fit_platform(file[1])
    with open(mm_path, 'r', encoding="utf-8") as f:
        content = f.read()

    regex = generate_command(pdf_path, "PAGE_NUM", other_platform)
    regex = re.escape(regex).replace("PAGE_NUM", '(\\d+)')
    new_content = re.sub(regex, switch_platform, content)

    if new_content != content:
        with open(mm_path, 'w', encoding="utf-8") as f:
            f.write(new_content)

for root, _, files in os.walk(path_fit_platform(config["bookxnote_root_windows"])):
    if os.path.dirname(root) == path_fit_platform(config["bookxnote_root_windows"]):
        with open(f"{root}/manifest.json", encoding='utf-8') as f:
            j = json.load(f)
        print(j)
        if platform_not_match(p := j['res'][0]['refpath']):
            j['res'][0]['refpath'] = func_dict[platform](p)
            with open(f"{root}/manifest.json", 'w', encoding='utf-8') as f:
                json.dump(j, f, ensure_ascii=False)
