import json
import shutil
import freeplane
import time
import re
import random
import lxml
import yaml
import argparse
from pdf_page_and_annot_linker import generate_command
from path_cross_platform import *


with open('text_files/config.yaml', encoding='utf-8') as f:
    config = yaml.full_load(f)
with open('text_files/filelist.yaml', encoding='utf-8') as f:
    filelist = yaml.full_load(f)


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
    def __init__(self, pdf_path, mm_path, default_color, pdf_name=None, docid=0):
        bookxnote_pdf_name = os.path.basename(pdf_path)[:-4]
        self.mm = freeplane.Mindmap(mm_path)
        self.mm_parent = os.path.dirname(mm_path)
        self.styles = self.mm.rootnode._node.find('.//map_styles')
        self.default_color = default_color
        self.pdf_name = pdf_name if pdf_name is not None else bookxnote_pdf_name
        self.note = f"{path_fit_platform(config['bookxnote_root_windows'])}/{bookxnote_pdf_name}"
        self.docid = docid
        self.maxid = 0
        self.regex = re.escape(generate_command(pdf_path, "PAGE_NUM")).replace('PAGE_NUM', r'(\d+)')

        os.makedirs(f"{self.note}/imgfiles", exist_ok=True)

    def style_to_color(self, style_name):
        if (style := self.styles.find(f".//stylenode[@TEXT='{style_name}']")) is not None:
            if (color := style.get('BACKGROUND_COLOR')) is not None and color != '#ffffff':
                return f"ff{color[1:]}"
            if (color := style.get('BORDER_COLOR')) is not None and color != '#ffffff':
                return f"ff{color[1:]}"
        return self.default_color

    def get_extra_json(self, node):
        plain_text = node.plaintext
        extra_json = {
            "content": get_original_text(node),
            "linecolor": self.style_to_color(node.style),
        }
        if hyperlink := node.hyperlink:
            if page_r := re.search(self.regex, hyperlink):
                if (textblocks := node._node.find('./textblocks')) is not None:
                    extra_json = {
                        "docid": self.docid,
                        "fillcolor": self.style_to_color(node.style),
                        "originaltext": get_original_text(node),
                        "type": 5,
                    }

                    text_blocks = []
                    for big_block in textblocks.iterfind('./blocks'):
                        blocks = {"text": plain_text, "length": len(plain_text), "rects": get_textblocks(big_block), "start": 1}
                        blocks["first"] = blocks['rects'][0]
                        blocks["last"] = blocks['rects'][-1]
                        text_blocks.append(blocks)
                    extra_json['textblocks'] = text_blocks
                page = int(page_r.group(1)) - 1
                extra_json['page'] = page
        return extra_json

    def walk(self, node):
        node_json = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),  # "2023-05-16 22:21:24"
            "id": self.maxid,
            "title": "",  # 在导出的.md中将 ###### - 替换为 ###则需要改为"title" : "-"
            "docid": 0,
            "type": 7,
            "page": -1,
            "uuid": f"{random.randint(0, 0xffffffffffffffffffffffffffffffff):x}",
        }
        extra_json = self.get_extra_json(node)
        self.maxid += 1

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

        return node_json

    def translate(self):
        tmp = {"EpubVersion": 2, "filepath": "", "floatingtheme": [], "folded": False, "notelinks": [],
               "scalingratio": 90, "title": self.pdf_name, "unimportant": [],
               "markups": self.walk(self.mm.rootnode)['markups'], 'maxid': self.maxid}  # self.walk(self.mm.rootnode)
        with open(f'{self.note}/markups.json', 'w', encoding='utf-8') as f:
            json.dump(tmp, f, ensure_ascii=False)


def parse_command_args():
    with open('text_files/default_args.yaml', encoding='utf-8') as f:
        default_args = yaml.full_load(f)['freeplane_to_bookxnote']
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--filelist-entry', nargs='?', default=default_args['filelist_entry'])
    arg_parser.add_argument('--pdf', nargs='?', default=default_args['pdf'])
    arg_parser.add_argument('--mm', nargs='?', default=default_args['mm'])
    arg_parser.add_argument('--default-color', nargs='?', default=default_args['color'])
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_command_args()
    if args.filelist_entry:
        mm, pdf, _ = filelist[args.filelist_entry]
    else:
        mm = args.mm
        pdf = args.pdf

    t = FreeplaneToBookxnote(path_fit_platform(pdf),
                             path_fit_platform(mm),
                             args.default_color)
    t.translate()

