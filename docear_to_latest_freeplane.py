import re
import urllib.request

acrobat_address = r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"
mm_address = r'C:\Users\SceneryMC\Docear\projects\test\literature_and_annotations.mm'
pdf_address = r'E:\学习资料\计算机\参考书\可能会读的书\数学\线性代数\Linear Algebra Done Right\(图灵数学·统计学丛书) Sheldon Axler - 线性代数应该这样学-人民邮电出版社 (2016).pdf'
hyperlink = r'project://181BF1A7D813BUY4OAN8U6I27YKD5SVHBUYL/repo/(图灵数学·统计学丛书)%20Sheldon%20Axler%20-%20线性代数应该这样学-人民邮电出版社%20(2016).pdf'
meta_char = r".^$*+?{}[]\|()"
for c in meta_char:
    hyperlink = hyperlink.replace(c, rf"\{c}")
hyperlink = hyperlink.replace(r'\\', '\\')


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
