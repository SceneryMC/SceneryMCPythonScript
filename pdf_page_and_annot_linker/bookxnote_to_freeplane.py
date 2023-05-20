import json

import freeplane
import lxml.etree as ET
import os

color_to_style = {"fffb8c00": '重要', 'ffe53935': '极其重要', 'ff0000cc': '图片', 'ffcc0099':'代码', 'ff00897b':'总结'}
color_dict = {"ref": "fillcolor", "nonref": "linecolor"}
text_dict = {"ref": "originaltext", "nonref": "content"}

pdf_path = '/mnt/E/学习资料/计算机/参考书/可能会读的书/Python/进阶/FluentPython/FluentPython2022.pdf'
pdf_name = os.path.basename(pdf_path)[:-8]
json_path = "/mnt/E/学习资料/bookxnote/notebooks/FluentPython2022/markups.json"


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



def add_a_node(object, old_node):
    node = old_node.add_child()
    node_type = "ref" if "textblocks" in object else "nonref"
    if style := color_to_style.get(object[color_dict[node_type]], ""):
        node.style = style
    if (page := object['page']) != -1:
        node.hyperlink = f"execute:_okular --unique -p {page} {pdf_path}"
    add_text(node, object[text_dict[node_type]])
    if node_type == "ref" and "content" in object:
        add_detail(node, object["content"])
    if "annotations" in object:
        for d in object["annotations"]:
            if d["style"] == 1:
                node.set_image(link=f'{pdf_name}_files/{d["content"]}', size=0.6)
            elif d["style"] == 0 and node_type == "nonref":
                add_detail(node, d["content"])
    return node


def json_to_freeplane(object, node):
    if isinstance(object, list):
        for item in object:
            json_to_freeplane(item, node)
    elif isinstance(object, dict):
        new_node = add_a_node(object, node)
        if 'markups' in object:
            json_to_freeplane(object['markups'], new_node)


mm = freeplane.Mindmap('/mnt/E/学习资料/计算机/参考书/可能会读的书/C++/入门/C++Primer/C++Primer.mm')
mm_new = freeplane.Mindmap()
for name, style in mm.styles.items():
    mm_new.add_style(name, style)
with open(json_path) as f:
    j = json.load(f)
json_to_freeplane(j['markups'], mm_new.rootnode)
mm_new.save("/mnt/E/学习资料/计算机/参考书/可能会读的书/Python/进阶/FluentPython/test.mm", encoding='utf-8')


