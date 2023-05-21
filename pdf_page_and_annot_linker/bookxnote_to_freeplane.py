import json
import freeplane
import lxml.etree as ET
import os

from path_Windows_to_Linux import path_Windows_to_Linux, isLinux
from mm_filelist import *
from pdf_page_and_annot_linker import t1, generate_t2


def add_text(node, text):
    if '<body>' not in text:
        node.plaintext = text
    else:
        _element = ET.Element("richcontent", TYPE='NODE')
        _html = ET.SubElement(_element, "html")
        _html.append(ET.XML(text))
        node._node.append(_element)


def add_detail(node, text):
    _element = ET.Element("richcontent", TYPE='DETAILS')
    _html = ET.SubElement(_element, "html")
    if '<body>' not in text:
        _body = ET.SubElement(_html, "body")
        _p = ET.SubElement(_body, "p")
        _p.text = text
    else:
        _html.append(ET.XML(text))
    node._node.append(_element)


class BooxnoteToFreeplane:
    color_to_style = {"fffb8c00": '重要', 'ffe53935': '极其重要', 'ff0000cc': '图片', 'ffcc0099': '代码',
                      'ff00897b': '总结'}
    color_dict = {"ref": "fillcolor", "nonref": "linecolor"}
    text_dict = {"ref": "originaltext", "nonref": "content"}


    def __init__(self, pdf_path, mm_path, json_path, pdf_name=None):
        bookxnote_pdf_name = os.path.basename(pdf_path)[:-4]
        self.pdf_path = pdf_path
        self.mm = freeplane.Mindmap()
        self.mm_path = mm_path
        self.pdf_name = pdf_name if pdf_name is not None else bookxnote_pdf_name
        self.json_path = json_path
        self.t2 = generate_t2(pdf_path)

    def add_a_node(self, object, parent_node):
        node = parent_node.add_child()
        node_type = "ref" if "textblocks" in object else "nonref"
        if style := BooxnoteToFreeplane.color_to_style.get(
                object[BooxnoteToFreeplane.color_dict[node_type]], ""):
            node.style = style
        if (page := object['page']) != -1:
            node.hyperlink = f"execute:{t1[isLinux]}{page}{self.t2[isLinux]}"
        add_text(node, object[BooxnoteToFreeplane.text_dict[node_type]])
        if node_type == "ref" and "content" in object:
            add_detail(node, object["content"])
        if "annotations" in object:
            for d in object["annotations"]:
                if d["style"] == 1:
                    node.set_image(link=f'{self.pdf_name}_files/{d["content"]}', size=0.6)
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
        with open(self.json_path, encoding='utf-8') as f:
            j = json.load(f)
        self.json_to_freeplane(j['markups'], self.mm.rootnode)
        self.mm.save(self.mm_path, encoding='utf-8')


if __name__ == '__main__':
    mm, pdf, _ = filelist['C++Primer']
    t = BooxnoteToFreeplane(path_Windows_to_Linux(pdf),
                            path_Windows_to_Linux(r"E:\学习资料\计算机\参考书\可能会读的书\C++\入门\C++Primer\test.mm"),
                            path_Windows_to_Linux(r"E:\学习资料\bookxnote\notebooks\C++Primer5edCN\markups.json"),
                            "C++Primer")
    t.translate()
