import json
import shutil
import freeplane
import lxml.etree, lxml.html
import os
import argparse
import yaml
from path_cross_platform import path_fit_platform
from pdf_page_and_annot_linker import generate_command

with open('text_files/filelist.yaml', encoding='utf-8') as f:
    filelist = yaml.full_load(f)


def remove_style_attribute(xml_node):
    for x in xml_node.iterfind('.//body[@style]'):
        x.attrib.pop('style')
    for x in xml_node.xpath('.//p[@style]'):
        x.attrib.pop('style')


def add_text(node, text):
    if '<body' not in text:
        node.plaintext = text.replace('\n', '&#xa;')
    else:
        _element = lxml.etree.Element("richcontent", TYPE='NODE')
        _html = lxml.etree.SubElement(_element, "html")
        _html.append(lxml.etree.fromstring(text))
        remove_style_attribute(_element)
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
    remove_style_attribute(_element)
    node._node.append(_element)


class BooxnoteToFreeplane:
    color_dict = {"ref": "fillcolor", "nonref": "linecolor"}
    text_dict = {"ref": "originaltext", "nonref": "content"}

    def __init__(self, pdf_path, mm_path, note_path, template, color_to_style):
        self.pdf_path = pdf_path
        self.mm = freeplane.Mindmap()
        self.mm_path = mm_path
        self.mm_name = os.path.basename(mm_path)[:-3]
        self.json_parent_path = note_path
        self.template = template
        self.color_to_style = color_to_style

        os.makedirs(f"{os.path.dirname(self.mm_path)}/{self.mm_name}_files", exist_ok=True)

    def save_textblocks(self, node, object):
        if (page := object['page']) != -1:
            node.hyperlink = f"execute:_{generate_command(self.pdf_path, page + 1)}"
            if 'textblocks' in object:
                text_blocks = lxml.etree.Element("textblocks")
                for big_block in object['textblocks']:
                    blocks = lxml.etree.Element("blocks")
                    text_blocks.append(blocks)
                    for r in big_block['rects']:
                        blocks.append(
                            lxml.etree.fromstring(f'<block x0="{r[0]}" y0="{r[1]}" width="{r[2]}" height="{r[3]}"/>'))
                node._node.append(text_blocks)

    def add_annotations(self, node, object, node_type):
        for d in object["annotations"]:
            if d["style"] == 1:
                node.set_image(link=f'{self.mm_name}_files/{d["content"]}', size=0.6)
                shutil.copy(f"{self.json_parent_path}/imgfiles/{d['content']}",
                            f"{os.path.dirname(self.mm_path)}/{self.mm_name}_files")
            elif d["style"] == 0 and node_type == "nonref":
                add_detail(node, d["content"])

    def add_a_node(self, object, parent_node):
        node = parent_node.add_child()
        node_type = "ref" if "textblocks" in object else "nonref"

        self.save_textblocks(node, object)
        add_text(node, object[BooxnoteToFreeplane.text_dict[node_type]])
        if node_type == "ref" and "content" in object:
            add_detail(node, object["content"])
        if "annotations" in object:
            self.add_annotations(node, object, node_type)
        if style := self.color_to_style.get(
                object[BooxnoteToFreeplane.color_dict[node_type]], ""):
            node.style = style

        return node

    def json_to_freeplane(self, object, parent_node):
        if isinstance(object, list):
            for item in object:
                self.json_to_freeplane(item, parent_node)
        elif isinstance(object, dict):
            this_node = self.add_a_node(object, parent_node)
            if 'markups' in object:
                self.json_to_freeplane(object['markups'], this_node)

    def copy_style(self):
        prop = self.mm.rootnode._node.find('.//properties')
        prop.set("associatedTemplateLocation", f'template:/{os.path.basename(self.template)}')
        styles = self.mm.rootnode._node.find('.//map_styles')
        new_styles = freeplane.Mindmap(self.template).rootnode._node.find('.//map_styles')
        styles.getparent().replace(styles, new_styles)

    def translate(self):
        self.copy_style()
        with open(f"{self.json_parent_path}/markups.json", encoding='utf-8') as f:
            j = json.load(f)
        self.json_to_freeplane(j['markups'], self.mm.rootnode)
        self.mm.save(self.mm_path, encoding='utf-8')


def parse_command_args():
    with open('text_files/default_args.yaml', encoding='utf-8') as f:
        default_args = yaml.full_load(f)['bookxnote_to_freeplane']
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--template', nargs='?', default=default_args['template'])
    arg_parser.add_argument('--filelist-entry', nargs='?', default=default_args['filelist_entry'])
    arg_parser.add_argument('--pdf', nargs='?', default=default_args['pdf'])
    arg_parser.add_argument('--mm', nargs='?', default=default_args['mm'])
    arg_parser.add_argument('--note', nargs='?', default=default_args['note'])
    arg_parser.add_argument('--color-to-style', nargs='*', default=default_args['color_to_style'])
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_command_args()
    if args.filelist_entry:
        mm, pdf, _ = filelist[args.filelist_entry]
    else:
        mm = args.mm
        pdf = args.pdf
    if not isinstance(arg_color_to_style := args.color_to_style, dict):
        arg_color_to_style = dict(zip(arg_color_to_style[::2], arg_color_to_style[1::2]))

    t = BooxnoteToFreeplane(path_fit_platform(pdf),
                            path_fit_platform(mm),
                            path_fit_platform(args.note),
                            path_fit_platform(args.template),
                            arg_color_to_style)
    t.translate()
