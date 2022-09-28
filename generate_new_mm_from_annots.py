import time
import random
import re
import html
import fitz
from pdf_page_and_annot_linker import isLinux, address_in_platform, t1, generate_t2

files = {

}
template_address = r"C:\Users\SceneryMC\AppData\Roaming\Freeplane\1.10.x\templates\xmind2021_default.mm"


def has_slash(serial):
    return "/" if (serial == len(toc) - 1 or toc[serial][0] >= toc[serial + 1][0]) else ""


def is_initial(serial):
    return 'POSITION="right"' if toc[serial][0] == 1 else ""


for file in files.values():
    with open(address_in_platform(template_address), encoding="utf-8") as f:
        s = f.read()
    s = s.replace('show_note_icons="true"',
                  'show_note_icons="true" associatedTemplateLocation="template:/xmind2021_default.mm"')

    doc = fitz.open(address_in_platform(file[1]))
    toc = doc.get_toc()
    t2 = generate_t2(file[1])

    new_line = []
    toc.append([1])
    for i in range(len(toc) - 1):
        timestamp = int(time.time() * 1000)
        new_line.append(
            f'<node TEXT="{html.escape(toc[i][1])}" {is_initial(i)} ID="ID_{random.randint(0, 0x7fffffff)}" '
            f'CREATED="{timestamp}" MODIFIED="{timestamp + 1}" '
            f'LINK="execute:_{t1[isLinux]}{toc[i][2]}{t2[isLinux]}"{has_slash(i)}>')

        next_indent_level = toc[i + 1][0]
        for _ in range(toc[i][0] - next_indent_level):
            new_line.append("</node>")
    CL = '\n'
    s = re.sub(r'<hook NAME="AutomaticEdgeColor" COUNTER="30" RULE="ON_BRANCH_CREATION"/>',
               f'<hook NAME="AutomaticEdgeColor" COUNTER="30" RULE="ON_BRANCH_CREATION"/>{CL}{CL.join(new_line)}', s)
    with open(address_in_platform(file[0]), 'w', encoding='utf-8') as f:
        f.write(s)
