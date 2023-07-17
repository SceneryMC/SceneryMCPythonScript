import json
import shutil
import freeplane
import lxml.etree, lxml.html
import os

from path_cross_platform import path_fit_platform
from mm_filelist import *
from pdf_page_and_annot_linker import generate_command


def add_text(node, text):
    if '<body' not in text:
        node.plaintext = text.replace('\n', '&#xa;')
    else:
        _element = lxml.etree.Element("richcontent", TYPE='NODE')
        _html = lxml.etree.SubElement(_element, "html")
        _html.append(lxml.etree.fromstring(text))
        node._node.append(_element)


def add_detail(node, text):
    _element = lxml.etree.Element("richcontent", TYPE='DETAILS')
    _html = lxml.etree.SubElement(_element, "html")
    if '<body' not in text:
        _body = lxml.etree.SubElement(_html, "body")
        for line in text.split('\n'):
            _p = lxml.etree.SubElement(_body, "p")
            _p.text = line
    else:
        _html.append(lxml.etree.fromstring(text))
    node._node.append(_element)


class BooxnoteToFreeplane:
    color_to_style = {'fffb8c00': '重要', 'ffe53935': '极其重要', 'ff0000cc': '图片', 'ffcc0099': '代码', 'ff00897b': '总结',
                      'fff89e02': '重要', 'ffff8280': '极其重要', 'ff59c6ff': '图片', }
    color_dict = {"ref": "fillcolor", "nonref": "linecolor"}
    text_dict = {"ref": "originaltext", "nonref": "content"}


    def __init__(self, pdf_path, mm_path, json_parent_path, pdf_name=None):
        bookxnote_pdf_name = os.path.basename(pdf_path)[:-4]
        self.pdf_path = pdf_path
        self.mm = freeplane.Mindmap()
        self.mm_path = mm_path
        self.pdf_name = pdf_name if pdf_name is not None else bookxnote_pdf_name
        self.json_parent_path = json_parent_path

        os.makedirs(f"{os.path.dirname(self.mm_path)}/{self.pdf_name}_files", exist_ok=True)

    def add_a_node(self, object, parent_node):
        node = parent_node.add_child()
        node_type = "ref" if "textblocks" in object else "nonref"
        if style := BooxnoteToFreeplane.color_to_style.get(
                object[BooxnoteToFreeplane.color_dict[node_type]], ""):
            node.style = style
        if (page := object['page']) != -1:
            node.hyperlink = f"execute:_{generate_command(self.pdf_path, page)}"
        add_text(node, object[BooxnoteToFreeplane.text_dict[node_type]])
        if node_type == "ref" and "content" in object:
            add_detail(node, object["content"])
        if "annotations" in object:
            for d in object["annotations"]:
                if d["style"] == 1:
                    node.set_image(link=f'{self.pdf_name}_files/{d["content"]}', size=0.6)
                    shutil.copy(f"{self.json_parent_path}/imgfiles/{d['content']}",
                                f"{os.path.dirname(self.mm_path)}/{self.pdf_name}_files")
                elif d["style"] == 0 and node_type == "nonref":
                    add_detail(node, d["content"])
        return node


    def json_to_freeplane(self, object, parent_node):
        if isinstance(object, list):
            for item in object:
                self.json_to_freeplane(item, parent_node)
        elif isinstance(object, dict):
            this_node = self.add_a_node(object, parent_node)
            if 'markups' in object:
                self.json_to_freeplane(object['markups'], this_node)


    def translate(self):
        with open(f"{self.json_parent_path}/markups.json", encoding='utf-8') as f:
            j = json.load(f)
        self.json_to_freeplane(j['markups'], self.mm.rootnode)
        self.mm.save(self.mm_path, encoding='utf-8')


if __name__ == '__main__':
    mm, pdf, _ = filelist['Java核心技术卷1']
    t = BooxnoteToFreeplane(path_fit_platform(pdf),
                            path_fit_platform('/mnt/E/学习资料/bookxnote/test.mm'),
                            path_fit_platform(r"E:\学习资料\bookxnote\notebooks\Java核心技术·卷I12ed"),
                            "Java核心技术·卷I12ed")
    t.translate()
