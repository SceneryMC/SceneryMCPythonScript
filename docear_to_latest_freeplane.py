import re
import urllib.request
import html
from pdf_page_and_annot_linker import acrobat_address

mm_address = r'E:\学习资料\计算机\参考书\可能会读的书\计算机系统\操作系统概念\操作系统概念.mm'
pdf_address = r'E:\学习资料\计算机\参考书\可能会读的书\计算机系统\操作系统概念\操作系统概念9th.pdf'
hyperlink = html.escape(r"project://181BF1A7D813BUY4OAN8U6I27YKD5SVHBUYL/../操作系统概念.pdf")


def add_cmd_command(match):
    end = match.end()

    page = re.search(r'.*?page="\d+"', mm_html_text[end:]).group()[:-1]
    page = page[page.rfind('"')+1:]
    url = f'"{acrobat_address}" /A "page={page}=OpenActions" "{pdf_address}"'

    return f'LINK="execute:_{urllib.request.quote(url)}"'


with open(mm_address, encoding='utf-8') as f:
    mm_html_text = f.read()

    mm_html_text = re.sub(rf'LINK="{hyperlink}"', add_cmd_command, mm_html_text)
with open(mm_address, 'w', encoding='utf-8') as f:
    f.writelines(mm_html_text)

# from PyPDF2 import PdfReader
#
# pdf_address = r"E:\学习资料\计算机\参考书\可能会读的书\算法\算法导论\3rd\算法导论（第3版）（中文版）[（美）Thomas.H.Cormen Charles.E.Leiserson Ronald.L.Rivest Clifford.Stein].pdf"
# reader = PdfReader("example.pdf")
#
#
# def _setup_page_id_to_num(pdf, pages=None, _result=None, _num_pages=None):
#     if _result is None:
#         _result = {}
#     if pages is None:
#         _num_pages = []
#         pages = pdf.trailer["/Root"].getObject()["/Pages"].getObject()
#     t = pages["/Type"]
#     if t == "/Pages":
#         for page in pages["/Kids"]:
#             _result[page.idnum] = len(_num_pages)
#             _setup_page_id_to_num(pdf, page.getObject(), _result, _num_pages)
#     elif t == "/Page":
#         _num_pages.append(1)
#     return _result
#
#
# def walk_bookmarks(elem, indent):
#     if isinstance(elem, list):
#         for sub_elem in elem:
#             walk_bookmarks(sub_elem, indent + 1)
#     else:
#         print(f"{'    ' * indent}{elem['/Title']}:{pg_id_num_map[elem.page.idnum] + 1}")
#
#
# pg_id_num_map = _setup_page_id_to_num(reader)
# walk_bookmarks(reader.outlines, -1)
