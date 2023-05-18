import json
import os
import shutil
import fitz
import freeplane
import time
import re
import random
from mm_filelist import filelist, bookxnote_root
from path_Windows_to_Linux import *

import lxml


def get_annot_blocks(page, serial, text):
    output = {"text": text, "length": len(text), "rects":[], "start": 0}
    annot = list(page.annots(types=[fitz.PDF_ANNOT_HIGHLIGHT]))[serial]
    points = annot.vertices
    for i in range(len(points) // 4):
        r = fitz.Quad(points[i * 4: i * 4 + 4]).rect
        output['rects'].append([r.x0, r.y0, r.width, r.height])
    output['first'] = output["rects"][0]
    output['last'] = output["rects"][-1]
    return [output]

def simplify_body(body):
    if all(y == 'p' or y == 'body' for y in [x.tag for x in body.iter()]):
        return "\n".join(x.strip() for x in body.itertext() if x.strip())
    else:
        return lxml.etree.tostring(body, encoding='utf-8').decode('utf-8')


def get_original_text(node):
    if (plain_text := node._node.get('TEXT')) is not None:
        return plain_text.strip()
    elif (rich_text := node._node.find("./richcontent[@TYPE='NODE']")) is not None:
        body = rich_text.find('html').find('body')
        return simplify_body(body)
    else:
        return ''


class FreeplaneToBookxnote:
    freeplane_style = {'重要': "fffb8c00", '极其重要': 'ffe53935', '图片': 'ff0000cc', '代码':'ffcc0099', '': 'ff59c6ff', '总结':'ff00897b'}
    def __init__(self, pdf_path, mm_path, bookxnote_root):
        self.pdf = fitz.open(pdf_path)
        self.mm = freeplane.Mindmap(mm_path)
        self.mm_parent = os.path.dirname(mm_path)
        self.pdf_name = os.path.basename(self.pdf.name)[:-4]
        self.note = f"{bookxnote_root}/{self.pdf_name}"
        self.docid = len(os.listdir(bookxnote_root)) - 2
        self.maxid = 0

    def walk(self, node):
        node_json = {
            "data": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  # "2023-05-16 22:21:24"
            "id": self.maxid,
            "type": 7,
            "page": -1,
            "uuid": f"{random.randint(0, 0xffffffffffffffffffffffffffffffff):x}",
        }

        plain_text = node.plaintext
        annot = re.match('P(\d+)-(\d+)', plain_text)
        if annot is None:
            extra_json = {
                "content": get_original_text(node),
                "linecolor": FreeplaneToBookxnote.freeplane_style[node.style],
            }
        else:
            page, serial = int(annot.group(1)) - 1, int(annot.group(2)) - 1
            extra_json = {
                "docid": self.docid,
                "fillcolor": "ffff8280",
                "originaltext": get_original_text(node),
                "page": page,
                "textblocks" : get_annot_blocks(self.pdf[page], serial, plain_text),
                "type": 5,
            }

        annotations = []
        if node.imagepath:
            shutil.copy(f"{self.mm_parent}/{node.imagepath}", f"{self.note}/imgfiles")
            annotations.append({"content":os.path.basename(node.imagepath) , "style": 1})
        if (detail := node._node.find("./richcontent[@TYPE='DETAILS']")) is not None:
            body = detail.find('html').find('body')
            if 'content' in extra_json:
                annotations.append({'content': simplify_body(body), 'style': 0})
            else:
                extra_json['content'] = simplify_body(body)
        node_json.update(extra_json)
        self.maxid += 1

        markups = []
        for child in node.children:
            markups.append(self.walk(child))
        if markups:
            node_json['markups'] = markups
        if annotations:
            node_json['annotations'] = annotations

        return node_json


    def translate(self):
        return {"EpubVersion": 2, "filepath": "", "floatingtheme": [], "folded": False, "notelinks": [],
                "scalingratio": 90, "title": self.pdf_name,
                "unimportant": [], "markups": self.walk(self.mm.rootnode)['markups'],
                }


if __name__ == '__main__':
    mm, pdf, _ = filelist['C++Primer']
    t = FreeplaneToBookxnote(path_Windows_to_Linux(pdf),
                             path_Windows_to_Linux(mm),
                             path_Windows_to_Linux(bookxnote_root))
    j = t.translate()
    with open(f'{t.note}/markups.json', 'w') as f:
        json.dump(j, f, ensure_ascii=False)
