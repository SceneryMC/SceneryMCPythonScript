import sys
import os
import re
import html
import itertools
import random
import urllib.request
import fitz
import yaml
import argparse
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lxml import etree
from PIL import Image
from path_cross_platform import *


# 读取配置文件
with open('text_files/config.yaml', encoding='utf-8') as f:
    config = yaml.full_load(f)
with open('text_files/filelist.yaml', encoding='utf-8') as f:
    filelist = yaml.full_load(f)
with open('text_files/error_correction_map.yaml', encoding='utf-8') as f:
    correct = yaml.full_load(f)
# 不可能用在他处的常量，别动就完事了
mat = fitz.Matrix(2, 2)
ns_re = {"re": "http://exslt.org/regular-expressions"}


def error_correction(s):
    # 按字替换与按词替换
    s = s.translate(str.maketrans(correct["character_error_correction"]))
    for original, correction in correct["word_error_correction"].items():
        s = s.replace(original, correction)
    return s


def mm_open_as_xml(mm_path: str) -> etree._ElementTree:
    with open(mm_path, encoding='utf-8') as f:
        # xml遇到&nbsp;会报错，直接粗暴的地转换为xml认识的形式
        s = f.read().replace("&nbsp;", "&#160;")
    return etree.fromstring(s)


def generate_command(pdf_path: str, page_num: int|str, pf=platform) -> str:
    # 生成跳转到pdf的命令，Window必须用quote
    command = config['command_template'][pf].replace("PAGE_NUM", str(page_num)).replace("PDF_PATH", path_fit_platform(pdf_path, pf))
    if pf == "Windows":
        command = urllib.request.quote(command)
    return command


def save_vertices(node, vertices):
    text_blocks = etree.Element("textblocks")
    blocks = etree.SubElement(text_blocks, "blocks")
    for i in range(len(vertices) // 4):
        r = fitz.Quad(vertices[i * 4: i * 4 + 4]).rect
        blocks.append(etree.fromstring(f'<block x0="{r.x0}" y0="{r.y0}" width="{r.width}" height="{r.height}"/>'))
    node.append(text_blocks)


def get_hightlighted_text(sep, annot, wordlist) -> str:
    words = []
    points = annot.vertices
    quad_count = len(points) // 4
    # 按Quad判断wordlist中的词是否属于选区
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4: i * 4 + 4]).rect
        for w in wordlist:
            tmp_rect = fitz.Rect(w[:4])
            tmp_intersect_rect = fitz.Rect(tmp_rect).intersect(r)
            if tmp_intersect_rect.get_area() > config["intersect_portion"] * min(tmp_rect.get_area(), r.get_area()):
                word = w[4]
                unit_length = (w[2] - w[0]) / len(word)
                start, end = round((r[0] - w[0]) / unit_length, 0), round((r[2] - w[0]) / unit_length, 0)
                words.append(word[max(0, int(start)):min(len(word), int(end))])
    return sep.join(words)


class PDFAnnotationLinker:
    def __init__(self, pdf_path: str, mm_path: str, mode: str='text', image_size: float=0.5):
        self.mm_base, self.mm_name = os.path.split(mm_path)
        self.pdf_path = pdf_path
        # 分词符，中文不存在，英文为空格。约定PDF主名结尾为CN表示为中文，否则为英文
        self.sep = '' if pdf_path[:-4].endswith("CN") else ' '
        # freeplane存储图片的文件夹的默认名
        self.image_folder = f"{self.mm_name[:-3]}_files"
        # text 或 image，前者适合自带文字层的PDF，使用文字层内容；后者适合OCR生成的文字层质量不高的PDF，直接截图
        self.mode = mode
        # 仅mode == image时有用，确定图片在mm中的默认缩放比
        self.image_size = image_size
        # 打开PDF和mm
        self.pdf = fitz.open(pdf_path)
        self.mm = mm_open_as_xml(mm_path)

    def get_new_endpoints(self) -> list[etree._Element]:
        # 查找没有样式（否则text不为tag，而为element.text）、没有添加LINK的新节点
        # 不同时retrun self.mm.xpath(f".//*[re:match(text(), '{endpoint_regex}')]", namespaces=ns_re)的结果：不允许添加样式
        return self.mm.xpath(f""".//*[re:match(@TEXT, '{config["endpoint_regex"]}') and not(@LINK)]""", namespaces=ns_re)

    def link_endpoints(self) -> None:
        endpoints = self.get_new_endpoints()
        for endpoint in endpoints:
            r = re.search(config['endpoint_regex'], endpoint.get('TEXT'))
            # element已经经过一次regex，这里能保证group1和group4有且仅有一个非None
            if r.group(1):
                self.link_full_endpoint(endpoint, int(r.group(2)) - 1, int(r.group(3)) - 1) # 从1开始转为从0开始
            else:
                self.link_simple_endpoint(endpoint, int(r.group(5)) - 1) # 从1开始转为从0开始

    def link_full_endpoint(self, endpoint: etree._Element, page_num: int, annot_num: int) -> None:
        print(f"P{page_num + 1}-{annot_num + 1}")
        # 不同mode调用不同的函数
        method_map = {"text": self.change_text, "image": self.add_image}

        page = self.pdf[page_num]
        command = generate_command(self.pdf_path, page_num + 1)
        # 获取annot_num指定的高亮，用itertools避免构建整个list
        annot = next(itertools.islice(page.annots(types=[fitz.PDF_ANNOT_HIGHLIGHT]), annot_num, None))
        annot_text = error_correction(annot.info['content'])

        # 调用mode对应的函数，text添加文字，image创建截图
        method_map[self.mode](page, annot, endpoint)
        # 将pdf高亮区域保存到mm中，以便转换回bookxnote
        save_vertices(endpoint, annot.vertices)

        # 添加跳转命令（method_map中不含此步）
        endpoint.set("LINK", f"execute:_{command}")
        # 添加节点明细
        if annot_text != '':
            detail = etree.fromstring(f'<richcontent CONTENT-TYPE="xml/" TYPE="DETAILS">\n'
                                      f'<html>\n\t<head>\n\n\t</head>\n\t<body>\n\t\t<p>{html.escape(annot_text)}</p>'
                                      f'\n\t</body>\n</html></richcontent>')
            endpoint.append(detail)

    def change_text(self, page, annot, endpoint: etree._Element) -> None:
        # 词列表
        wordlist = page.get_text("words")
        # 先y后x，升序排列
        wordlist.sort(key=lambda w: tuple(w[5:]))
        highlight = error_correction(get_hightlighted_text(self.sep, annot, wordlist))
        endpoint.set("TEXT", f'{endpoint.get("TEXT")} {html.escape(highlight)}')

    def add_image(self, page, annot, endpoint: etree._Element) -> None:
        # annot.vertices内容：[(x0, y0), ...]
        # 获取四个边界的位置
        x = [p[0] for p in annot.vertices]
        y = [p[1] for p in annot.vertices]
        l, u, r, b = min(x), min(y), max(x), max(y)

        # 由边界创建白背景（否则为空背景）
        plane = Image.new('RGB', (int((r - l) * config["length_to_pixel"]), int((b - u) * config["length_to_pixel"])), color="white")
        points = annot.vertices
        quad_count = len(points) // 4
        # 将文字按Quad截图，粘贴到白背景上
        for i in range(quad_count):
            clip = fitz.Quad(points[i * 4: i * 4 + 4]).rect
            pix = page.get_pixmap(matrix=mat, clip=clip, annots=False)
            plane.paste(Image.frombytes('RGB', (pix.width, pix.height), pix.samples),
                        (int((clip.x0 - l) * config["length_to_pixel"]), int((clip.y0 - u) * config["length_to_pixel"])))

        # 生成图片文件，并在当前节点上添加该图片
        png_filename = f"png_{random.randrange(0, 0xffffffffffff)}.png"
        img_tag = etree.fromstring(f'<hook URI="{self.image_folder}/{png_filename}" SIZE="{image_size}" '
                                   f'NAME="ExternalObject"/>')
        endpoint.append(img_tag)
        plane.save(f"{self.mm_base}/{self.image_folder}/{png_filename}", quality=100)

    def link_simple_endpoint(self, endpoint: etree._Element, page_num: int) -> None:
        print(f"p{page_num + 1}")

        command = generate_command(self.pdf_path, page_num + 1)
        endpoint.set("LINK", f"execute:_{command}")

    def save(self) -> None:
        with open(os.path.join(self.mm_base, self.mm_name), 'w', encoding='utf-8') as f:
            f.write(etree.tounicode(self.mm))


def parse_command_args():
    with open('text_files/default_args.yaml', encoding='utf-8') as f:
        default_args = yaml.full_load(f)['pdf_page_and_annot_linker']
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--filelist-entry', nargs='?', default=default_args['filelist_entry'])
    arg_parser.add_argument('--pdf', nargs='?', default=default_args['pdf'])
    arg_parser.add_argument('--mm', nargs='?', default=default_args['mm'])
    arg_parser.add_argument('--image-size', nargs='?', type=float, default=default_args['image_size'])
    arg_parser.add_argument('--mode', nargs='?',choices=['text', 'image'], default=default_args['mode'])
    return arg_parser.parse_args()


if __name__ == '__main__':
    args = parse_command_args()
    if args.filelist_entry:
        mm, pdf, image_size = filelist[args.filelist_entry]
    else:
        mm = args.mm
        pdf = args.pdf
        image_size = args.image_size

    p = PDFAnnotationLinker(path_fit_platform(pdf),
                            path_fit_platform(mm),
                            args.mode, image_size)
    p.link_endpoints()
    p.save()

