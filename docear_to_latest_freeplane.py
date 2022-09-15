import re
import urllib.request
from pdf_page_and_annot_linker import acrobat_address, filelist

mm_address, pdf_address = filelist['机器学习']


def add_cmd_command(match):
    end = match.end()

    page = re.search(r'.*?page="\d+"', mm_html_text[end:]).group()[:-1]
    page = page[page.rfind('"')+1:]
    url = f'"{acrobat_address}" /A "page={page}=OpenActions" "{pdf_address}"'

    return f'LINK="execute:_{urllib.request.quote(url)}"'


with open(mm_address, encoding='utf-8') as f:
    mm_html_text = f.read()

    mm_html_text = re.sub(rf'LINK="project://\w+/.+?\.pdf"', add_cmd_command, mm_html_text)
    mm_html_text = re.sub(rf"\n<pdf_annotation .*?/>", "", mm_html_text, 0)
    mm_html_text = re.sub(rf"\n<pdf_annotation .*?</pdf_annotation>", "", mm_html_text, 0, re.DOTALL)
with open(mm_address, 'w', encoding='utf-8') as f:
    f.writelines(mm_html_text)
