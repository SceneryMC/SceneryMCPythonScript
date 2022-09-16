import time
import random
import re
import html
import fitz
from pdf_page_and_annot_linker import isLinux, address_in_platform, t1, generate_t2

files = {
    "Linux命令行与shell脚本编程大全": (r"E:\学习资料\计算机\参考书\可能会读的书\Linux\Linux命令行与shell脚本编程大全\Linux命令行与shell脚本编程大全.mm",
                        r"E:\学习资料\计算机\参考书\可能会读的书\Linux\Linux命令行与shell脚本编程大全\Linux命令行与shell脚本编程大全3edCN.pdf"),
}
template_address = r"C:\Users\SceneryMC\AppData\Roaming\Freeplane\1.10.x\templates\xmind2021_default.mm"


def has_slash(serial):
    if serial == len(toc) - 1 or toc[serial][0] >= toc[serial + 1][0]:
        return "/"
    else:
        return ""


def is_initial(serial):
    if toc[serial][0] == 1:
        return 'POSITION="right"'
    else:
        return ""


for file in files.values():
    with open(address_in_platform(template_address), encoding="utf-8") as f:
        s = f.read()
    s = s.replace('show_note_icons="true"',
                  'show_note_icons="true" associatedTemplateLocation="template:/xmind2021_default.mm"')

    doc = fitz.open(address_in_platform(file[1]))
    toc = doc.get_toc()
    t2 = generate_t2(file[1])

    new_line = []
    for i in range(len(toc)):
        new_line.append(f'<node TEXT="{html.escape(toc[i][1])}" {is_initial(i)} ID="ID_{random.randint(0, 0x7fffffff)}" '
                        f'CREATED="{int(time.time() * 1000)}" MODIFIED="{int(time.time() * 1000) + 1}" '
                        f'LINK="execute:_{t1[isLinux]}{toc[i][2]}{t2[isLinux]}"{has_slash(i)}>')

        if i == len(toc) - 1:
            next = 1
        else:
            next = toc[i + 1][0]
        for _ in range(toc[i][0] - next):
            new_line.append("</node>")
    CL = '\n'
    s = re.sub(r'<hook NAME="AutomaticEdgeColor" COUNTER="30" RULE="ON_BRANCH_CREATION"/>',
               f'<hook NAME="AutomaticEdgeColor" COUNTER="30" RULE="ON_BRANCH_CREATION"/>{CL}{CL.join(new_line)}', s)
    with open(address_in_platform(file[0]), 'w', encoding='utf-8') as f:
        f.write(s)
