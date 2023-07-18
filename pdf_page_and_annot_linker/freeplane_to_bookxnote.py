import json
import shutil
import freeplane
import time
import re
import random
import lxml
from pdf_page_and_annot_linker import generate_command
from mm_filelist import filelist, bookxnote_root_windows
from path_cross_platform import *


def get_textblocks(big_block):
    rects = []
    for r in big_block.iterfind('./block'):
        rects.append([float(r.get('x0')), float(r.get('y0')), float(r.get('width')), float(r.get('height'))])
    return rects


def get_simplest_text(body):
    if all(y == 'p' or y == 'body' for y in [x.tag for x in body.iter()]):
        return "\n".join(x.strip() for x in body.itertext() if x.strip())
    else:
        return lxml.etree.tostring(body, encoding='utf-8').decode('utf-8')


def get_original_text(node):
    if (plain_text := node._node.get('TEXT')) is not None:
        return plain_text.strip()
    elif (rich_text := node._node.find("./richcontent[@TYPE='NODE']")) is not None:
        body = rich_text.find('html').find('body')
        return get_simplest_text(body)
    else:
        return ''


class FreeplaneToBookxnote:
    freeplane_style = {'重要': "fffb8c00", '极其重要': 'ffe53935', '图片': 'ff0000cc', '代码':'ffcc0099', '': 'fffeeb73', '总结':'ff00897b'}
    def __init__(self, pdf_path, mm_path, bookxnote_root, pdf_name=None, docid=0):
        bookxnote_pdf_name = os.path.basename(pdf_path)[:-4]
        self.mm = freeplane.Mindmap(mm_path)
        self.mm_parent = os.path.dirname(mm_path)
        self.pdf_name = pdf_name if pdf_name is not None else bookxnote_pdf_name
        self.note = f"{bookxnote_root}/{bookxnote_pdf_name}"
        self.docid = docid
        self.maxid = 0
        self.regex = re.escape(generate_command(pdf_path, "PAGE_NUM")).replace('PAGE_NUM', r'(\d+)')

        os.makedirs(f"{self.note}/imgfiles", exist_ok=True)

    def get_extra_json(self, node):
        plain_text = node.plaintext
        extra_json = {
            "content": get_original_text(node),
            "linecolor": FreeplaneToBookxnote.freeplane_style[node.style],
        }
        if hyperlink := node.hyperlink:
            if page_r := re.search(self.regex, hyperlink):
                if (textblocks := node._node.find('./textblocks')) is not None:
                    page = int(page_r.group(1))
                    extra_json = {
                        "docid": self.docid,
                        "fillcolor": FreeplaneToBookxnote.freeplane_style[node.style],
                        "originaltext": get_original_text(node),
                        "page": page,
                        "type": 5,
                    }

                    text_blocks = []
                    for big_block in textblocks.iterfind('./blocks'):
                        blocks = {"text": plain_text, "length": len(plain_text), "rects": get_textblocks(big_block), "start": 1}
                        blocks["first"] = blocks['rects'][0]
                        blocks["last"] = blocks['rects'][-1]
                        text_blocks.append(blocks)
                    extra_json['textblocks'] = text_blocks
        return extra_json

    def walk(self, node):
        node_json = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  # "2023-05-16 22:21:24"
            "id": self.maxid,
            "title": "-",  # 在导出的.md中将 ###### - 替换为 ###
            "type": 7,
            "page": -1,
            "uuid": f"{random.randint(0, 0xffffffffffffffffffffffffffffffff):x}",
        }
        extra_json = self.get_extra_json(node)

        annotations = []
        if node.imagepath:
            shutil.copy(f"{self.mm_parent}/{node.imagepath}", f"{self.note}/imgfiles")
            annotations.append({"content":os.path.basename(node.imagepath) , "style": 1})
        if (detail := node._node.find("./richcontent[@TYPE='DETAILS']")) is not None:
            body = detail.find('html').find('body')
            if 'content' in extra_json:
                annotations.append({'content': get_simplest_text(body), 'style': 0})
            else:
                extra_json['content'] = get_simplest_text(body)
        node_json.update(extra_json)
        if annotations:
            node_json['annotations'] = annotations

        markups = []
        for child in node.children:
            markups.append(self.walk(child))
        if markups:
            node_json['markups'] = markups

        self.maxid += 1
        return node_json


    def translate(self):
        tmp = {"EpubVersion": 2, "filepath": "", "floatingtheme": [], "folded": False, "notelinks": [],
               "scalingratio": 90, "title": self.pdf_name, "unimportant": [],
               "markups": self.walk(self.mm.rootnode)['markups'], 'maxid': self.maxid}  # self.walk(self.mm.rootnode)
        print(self.maxid)
        return tmp


if __name__ == '__main__':
    mm, pdf, _ = filelist['FluentPython']
    t = FreeplaneToBookxnote(path_fit_platform(pdf),
                             path_fit_platform(mm),
                             path_fit_platform(bookxnote_root_windows),
                             )
    j = t.translate()
    with open(f'{t.note}/markups.json', 'w', encoding='utf-8') as f:
        json.dump(j, f, ensure_ascii=False)
