import re
import shutil
import lxml.etree
import fitz
from pdf_page_and_annot_linker import save_vertices
from mm_filelist import filelist

for value in filelist.values():
    print(value[1])
    path = value[0]
    # shutil.copy(path, rf"E:\学习资料\bookxnote\backups/")
    pdf = fitz.open(value[1])
    with open(path, encoding='utf-8') as f:
        s = f.read().replace("&nbsp;", "&#160;")
    xml_tree = lxml.etree.fromstring(s)
    for node in xml_tree.iterfind('.//node'):
        if not (text := node.get("TEXT")):
            if (result := node.find('./richcontent[@TYPE="NODE"]')) is not None:
                t_ls = []
                for t in result.itertext():
                    t_ls.append(t)
                text = ''.join(t_ls)
        if (r := re.search(r"P(\d+)-(\d+)", text)) and node.find('./textblocks') is None:
            page_num, annot_num = int(r.group(1)) - 1, int(r.group(2)) - 1
            page = pdf[page_num]
            ls = list(page.annots(types=[fitz.PDF_ANNOT_HIGHLIGHT]))
            if len(ls) > annot_num:
                print(page_num + 1, annot_num + 1)
                annot = ls[annot_num]
                save_vertices(node, annot.vertices)
    with open(path, 'wb') as f:
        f.write(lxml.etree.tostring(xml_tree, encoding='utf-8'))