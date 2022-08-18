import re
import urllib.request
import fitz
from error_correction_dictionary import character_error_correction, word_error_correction

acrobat_address = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
mm_address = r"/media/scenerymc/本地磁盘/学习资料/计算机/参考书/可能会读的书/算法/算法导论/整理/CLRS.mm"
pdf_address_open = r"/media/scenerymc/本地磁盘/学习资料/计算机/参考书/可能会读的书/算法/算法导论/4th/Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein - Introduction to Algorithms-The MIT Press (2022).pdf"
pdf_address_to = r"E:\学习资料\计算机\参考书\可能会读的书\算法\算法导论\4th\Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein - Introduction to Algorithms-The MIT Press (2022).pdf"
intersect_portion = 0.5


def _parse_highlight(annot, wordlist):
    points = annot.vertices
    quad_count = int(len(points) / 4)
    sentences = ['' for _ in range(quad_count)]
    for i in range(quad_count):
        r = fitz.Quad(points[i * 4: i * 4 + 4]).rect
        words = []
        for w in wordlist:
            tmp_rect = fitz.Rect(w[:4])
            tmp_intersect_rect = fitz.Rect(tmp_rect).intersect(r)
            tmp_rect.get_area(), tmp_intersect_rect.get_area()
            if tmp_intersect_rect.get_area() > intersect_portion * tmp_rect.get_area():
                words.append(w)
        sentences[i] = ' '.join(w[4] for w in words)
    sentence = [char for char in ''.join(sentences)]
    for i in range(len(sentence)):
        sentence[i] = character_error_correction.get(sentence[i], sentence[i])
    sentence = ''.join(sentence)
    for original, correction in word_error_correction:
        sentence = sentence.replace(original, correction)
    return sentence


def get_highlight_and_annot(mupdf_page, annot_num):
    wordlist = mupdf_page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: tuple(w[5:]))  # ascending y, then x
    for annot in mupdf_page.annots():
        annot_num -= 1
        if annot_num == 0 and annot.type[0] == 8:
            return annot.info['content'], _parse_highlight(annot, wordlist)


def add_cmd_command(match):
    text = match.group()
    if 'LINK' in text:
        return text

    page = re.search(r"(p\d+|P\d+-\d+)", text).group()[1:].split('-')
    print(page)
    url = f'"{acrobat_address}" /A "page={page[0]}=OpenActions" "{pdf_address_to}"'
    left = right = -1 - (text[-2] == '/')
    details = ""
    if text[6] == 'P' and len(page) == 2:
        annot, highlight = get_highlight_and_annot(doc[int(page[0])-1], int(page[1]))
        text = text.replace(f'P{page[0]}-{page[1]}"', f'P{page[0]}-{page[1]} {highlight}"')
        if annot != '':
            details = f'<richcontent CONTENT-TYPE="xml/" TYPE="DETAILS">\n' \
                  f'<html>\n\t<head>\n\n\t</head>\n\t<body>\n\t\t<p>{annot}</p>\n\t</body>\n</html></richcontent>'
            if right == -2:
                right = -1
                details += "</node>"

    return f'{text[:left]} LINK="execute:_{urllib.request.quote(url)}"{text[right:]}{details}'


doc = fitz.open(pdf_address_open)
with open(mm_address, encoding='utf-8') as f:
    mm_html_text_backup = f.read()
    mm_html_text = re.sub(r'TEXT="(p\d+|P\d+-\d+)".*?>', add_cmd_command, mm_html_text_backup)
with open(mm_address, 'w', encoding='utf-8') as f:
    f.writelines(mm_html_text)

