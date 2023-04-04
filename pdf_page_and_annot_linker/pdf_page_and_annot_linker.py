import sys
import os
import re
import urllib.request
import html
import itertools
import random
import fitz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PIL import Image
from error_correction_dictionary import character_error_correction, word_error_correction
from path_Windows_to_Linux import *
from mm_filelist import filelist

intersect_portion = 0.3
length_to_pixel = 2.05
mat = fitz.Matrix(2, 2)
acrobat_path = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
t1 = (urllib.request.quote(f'"{acrobat_path}" /A "page='), 'okular --unique -p ')


def generate_t2(pdf_path):
    return (urllib.request.quote(f'=OpenActions" "{path_Windows_to_Linux(pdf_path, False)}"'),
            f' {path_Windows_to_Linux(pdf_path, True)}')


def error_correction(s):
    s = s.translate(str.maketrans(character_error_correction))
    for original, correction in word_error_correction.items():
        s = s.replace(original, correction)
    return s


def parse_highlight(annot, wordlist):
    words = []
    points = annot.vertices
    quad_count = len(points) // 4
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4: i * 4 + 4]).rect
        for w in wordlist:
            tmp_rect = fitz.Rect(w[:4])
            tmp_intersect_rect = fitz.Rect(tmp_rect).intersect(r)
            if tmp_intersect_rect.get_area() > intersect_portion * min(tmp_rect.get_area(), r.get_area()):
                word = w[4]
                unit_length = (w[2] - w[0]) / len(word)
                start, end = round((r[0] - w[0]) / unit_length, 0), round((r[2] - w[0]) / unit_length, 0)
                words.append(word[max(0, int(start)):min(len(word), int(end))])
    return sep.join(words)


def add_cmd_command(match):
    text = match.group()
    if 'LINK' in text:
        return text

    page = re.search(r"(p\d+|P\d+-\d+)", text).group()[1:].split('-')
    print(page)
    url = f'{t1[isLinux]}{page[0]}{t2[isLinux]}'
    left = right = -1 - (text[-2] == '/')
    details = ""
    if text[6] == 'P' and len(page) == 2:
        mupdf_page, annot_num = doc[int(page[0]) - 1], int(page[1]) - 1
        annot = next(itertools.islice(mupdf_page.annots(types=[fitz.PDF_ANNOT_HIGHLIGHT]), annot_num, None))
        annot_text = error_correction(annot.info['content'])
        if mode == 'text':
            wordlist = mupdf_page.get_text("words")  # list of words on page
            wordlist.sort(key=lambda w: tuple(w[5:]))  # ascending y, then x
            highlight = error_correction(parse_highlight(annot, wordlist))
            text = text.replace(f'P{page[0]}-{page[1]}"', f'P{page[0]}-{page[1]} {html.escape(highlight)}"')
        elif mode == 'image':
            x = [p[0] for p in annot.vertices]
            y = [p[1] for p in annot.vertices]
            l, u, r, b = min(x), min(y), max(x), max(y)
            plane = Image.new('RGB', (int((r - l) * length_to_pixel), int((b - u) * length_to_pixel)), color="white")
            points = annot.vertices
            quad_count = len(points) // 4
            for i in range(quad_count):
                clip = fitz.Quad(points[i * 4: i * 4 + 4]).rect
                pix = mupdf_page.get_pixmap(matrix=mat, clip=clip, annots=False)
                plane.paste(Image.frombytes('RGB', (pix.width, pix.height), pix.samples),
                            (int((clip.x0 - l) * length_to_pixel), int((clip.y0 - u) * length_to_pixel)))
            png_filename = f"png_{random.randrange(0, 0xffffffffffff)}.png"
            details += f'<hook URI="{image_folder}/{png_filename}" SIZE="{image_size}" NAME="ExternalObject"/>'
            plane.save(f"{mm_base}/{image_folder}/{png_filename}", quality=100)

        if annot_text != '':
            details += f'<richcontent CONTENT-TYPE="xml/" TYPE="DETAILS">\n' \
                       f'<html>\n\t<head>\n\n\t</head>\n\t<body>\n\t\t<p>{html.escape(annot_text)}</p>\n\t</body>\n</html></richcontent>'
        if right == -2:
            right = -1
            details += "</node>"

    return f'{text[:left]} LINK="execute:_{url}"{text[right:]}{details}'


def get_args(args):
    if args[2] in filelist:
        mm_path, pdf_path, image_size = filelist[args[2]]
    else:
        mm_path = args[2]
        pdf_path = args[3]
        image_size = float(args[4])
    return args[1], mm_path, pdf_path, image_size


if __name__ == '__main__':
    mode, mm_path, pdf_path, image_size = get_args(sys.argv)
    sep = '' if pdf_path[:-4].endswith("CN") else ' '
    t2 = generate_t2(pdf_path)
    mm_base, mm_name = os.path.split(path_Windows_to_Linux(mm_path))
    image_folder = f"{mm_name[:-3]}_files"

    doc = fitz.open(path_Windows_to_Linux(pdf_path))
    with open(path_Windows_to_Linux(mm_path), encoding='utf-8') as f:
        mm_html_text_backup = f.read()
        mm_html_text = re.sub(r'TEXT="(p\d+|P\d+-\d+)".*?>', add_cmd_command, mm_html_text_backup)
    if not mm_html_text == mm_html_text_backup:
        with open(path_Windows_to_Linux(mm_path), 'w', encoding='utf-8') as f:
            f.writelines(mm_html_text)
