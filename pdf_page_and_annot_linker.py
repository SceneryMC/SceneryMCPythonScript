import re
import urllib.request
import html
import fitz
import platform
from error_correction_dictionary import character_error_correction, word_error_correction

isLinux = (platform.system().lower() == "linux")
intersect_portion = 0.5
filelist = {
    "CLRS": (r"E:\学习资料\计算机\参考书\可能会读的书\算法\算法导论\CLRS.mm",
             r"E:\学习资料\计算机\参考书\可能会读的书\算法\算法导论\CLRS4ed.pdf"),
    "ITLA": (r"E:\学习资料\计算机\参考书\可能会读的书\数学\线性代数\ITLA\ITLA.mm",
             r"E:\学习资料\计算机\参考书\可能会读的书\数学\线性代数\ITLA\ITLA5ed.pdf"),
    "LADR": (r"E:\学习资料\计算机\参考书\可能会读的书\数学\线性代数\LADR\LADR.mm",
             r"E:\学习资料\计算机\参考书\可能会读的书\数学\线性代数\LADR\LADR3edCN.pdf"),
    "CppPrimer": (r"E:\学习资料\计算机\参考书\可能会读的书\Cpp\入门\CppPrimer\CppPrimer.mm",
                  r"E:\学习资料\计算机\参考书\可能会读的书\Cpp\入门\CppPrimer\CppPrime5edCN.pdf"),
    "C专家编程": (r"E:\学习资料\计算机\参考书\可能会读的书\C\进阶\C专家编程\C专家编程.mm",
                  r"E:\学习资料\计算机\参考书\可能会读的书\C\进阶\C专家编程\C专家编程.pdf"),
    "深入理解计算机系统": (r"E:\学习资料\计算机\参考书\可能会读的书\计算机系统\深入理解计算机系统\深入理解计算机系统.mm",
                        r"E:\学习资料\计算机\参考书\可能会读的书\计算机系统\深入理解计算机系统\深入理解计算机系统3edCN.pdf"),
    "操作系统导论": (r"E:\学习资料\计算机\参考书\可能会读的书\计算机系统\操作系统导论\操作系统导论.mm",
                     r"E:\学习资料\计算机\参考书\可能会读的书\计算机系统\操作系统导论\操作系统导论2019CN.pdf"),
    "操作系统概念": (r"E:\学习资料\计算机\参考书\可能会读的书\计算机系统\操作系统概念\操作系统概念.mm",
                     r"E:\学习资料\计算机\参考书\可能会读的书\计算机系统\操作系统概念\操作系统概念9edCN.pdf"),

}


def address_in_platform(addr, wtl=isLinux):
    if not wtl:
        return addr
    addr = addr.replace(":", "")
    addr = addr.replace("\\", "/")
    return f"/mnt/{addr}"


def error_correction(s):
    for i in range(len(s)):
        s[i] = character_error_correction.get(s[i], s[i])

    i = 1
    while i < len(s) - 1:
        if (not (0 <= ord(s[i - 1]) <= 127) or not (0 <= ord(s[i + 1]) <= 127)) and s[i] == ' ':
            s.pop(i)
        i += 1
    s = ''.join(s)

    for original, correction in word_error_correction:
        s = s.replace(original, correction)

    return s


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
    return [char for char in ''.join(sentences)]


def get_highlight_and_annot(mupdf_page, annot_num):
    wordlist = mupdf_page.get_text("words")  # list of words on page
    wordlist.sort(key=lambda w: tuple(w[5:]))  # ascending y, then x
    for annot in mupdf_page.annots():
        annot_num -= 1
        if annot_num == 0 and annot.type[0] == 8:
            return error_correction([i for i in annot.info['content']]), \
                   error_correction(_parse_highlight(annot, wordlist))


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
        annot, highlight = get_highlight_and_annot(doc[int(page[0]) - 1], int(page[1]))
        text = text.replace(f'P{page[0]}-{page[1]}"', f'P{page[0]}-{page[1]} {html.escape(highlight)}"')
        if annot != '':
            details = f'<richcontent CONTENT-TYPE="xml/" TYPE="DETAILS">\n' \
                      f'<html>\n\t<head>\n\n\t</head>\n\t<body>\n\t\t<p>{html.escape(annot)}</p>\n\t</body>\n</html></richcontent>'
            if right == -2:
                right = -1
                details += "</node>"

    return f'{text[:left]} LINK="execute:_{url}"{text[right:]}{details}'


acrobat_address = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
file = filelist["C专家编程"]
t1 = [urllib.request.quote(f'"{acrobat_address}" /A "page='), 'evince -i ']
t2 = [urllib.request.quote(f'=OpenActions" "{address_in_platform(file[1], False)}"'),
      f' {address_in_platform(file[1], True)}']
if __name__ == '__main__':
    doc = fitz.open(address_in_platform(file[1]))
    with open(address_in_platform(file[0]), encoding='utf-8') as f:
        mm_html_text_backup = f.read()
        mm_html_text = re.sub(r'TEXT="(p\d+|P\d+-\d+)".*?>', add_cmd_command, mm_html_text_backup)
    with open(address_in_platform(file[0]), 'w', encoding='utf-8') as f:
        f.writelines(mm_html_text)
