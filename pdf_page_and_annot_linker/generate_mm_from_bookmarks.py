import math
import fitz
import freeplane
import yaml
from path_cross_platform import *
from pdf_page_and_annot_linker import generate_command

files = {
"Java核心技术卷1": (r"E:\学习资料\计算机\参考书\可能会读的书\Java\入门\Java核心技术\Java核心技术卷1_test.mm",
                        r"E:\学习资料\计算机\参考书\可能会读的书\Java\入门\Java核心技术\Java核心技术·卷I12ed.pdf", 0.5),
}
with open('text_files/config.yaml') as f:
    template_address = path_fit_platform(yaml.full_load(f)["template_path_windows"])


class GenerateMM:
    def __init__(self, mm_path, pdf_path, with_annot):
        self.pdf_path = pdf_path
        self.mm_path = mm_path
        self.with_annot = with_annot
        self.doc = fitz.open(path_fit_platform(self.pdf_path))
        self.toc = self.doc.get_toc()

    def generate(self):
        mm = freeplane.Mindmap(template_address)
        prop = mm.rootnode._node.find('.//properties')
        prop.set("associatedTemplateLocation", 'template:/xmind2021_default.mm')
        self.add_node(mm.rootnode)
        mm.save(self.mm_path, encoding='utf-8')

    def add_node(self, root):
        stack = [root]
        toc_ls = self.toc + [[1, 0, 999999]]
        for i in range(len(self.toc)):
            node = stack[-1].add_child()
            node.plaintext = self.toc[i][1]
            node.hyperlink = f"execute:_{generate_command(self.pdf_path, self.toc[i][2])}"
            if (diff := toc_ls[i][0] - toc_ls[i + 1][0]) > 0:
                stack = stack[:-diff]
            elif toc_ls[i][0] < toc_ls[i + 1][0]:
                stack.append(node)
            if self.with_annot:
                self.add_annot(toc_ls[i][2], toc_ls[i + 1][2])

    def add_annot(self, begin, end):
        pass


if __name__ == '__main__':
    for file in files.values():
        t = GenerateMM(path_fit_platform(file[0]), path_fit_platform(file[1]), False)
        t.generate()
