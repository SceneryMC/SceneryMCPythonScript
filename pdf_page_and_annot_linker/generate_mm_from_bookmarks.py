import fitz
import freeplane
import yaml
from collections import defaultdict
from path_cross_platform import *
from pdf_page_and_annot_linker import generate_command


with open('text_files/config.yaml', encoding='utf-8') as f:
    template_address = path_fit_platform(yaml.full_load(f)["template_path_windows"])


class GenerateMM:
    def __init__(self, mm_path, pdf_path, with_annot):
        self.pdf_path = pdf_path
        self.mm_path = mm_path
        self.with_annot = with_annot
        self.pdf = fitz.open(path_fit_platform(self.pdf_path))
        self.toc = self.pdf.get_toc()
        self.belongs_to_previous_page = 0

    def generate(self):
        mm = freeplane.Mindmap(template_address)
        prop = mm.rootnode._node.find('.//properties')
        prop.set("associatedTemplateLocation", 'template:/xmind2021_default.mm')
        self.add_node(mm.rootnode)
        mm.save(self.mm_path, encoding='utf-8')

    def add_node(self, root):
        stack = [root]
        toc_ls = self.toc + [[1, "NOTEXISTS", len(self.pdf) - 1]]
        for i in range(len(self.toc)):
            node = stack[-1].add_child()
            node.plaintext = self.toc[i][1]
            node.hyperlink = f"execute:_{generate_command(self.pdf_path, self.toc[i][2])}"
            if (diff := toc_ls[i][0] - toc_ls[i + 1][0]) > 0:
                stack = stack[:-diff]
            elif toc_ls[i][0] < toc_ls[i + 1][0]:
                stack.append(node)
            if self.with_annot and toc_ls[i][2] <= toc_ls[i + 1][2]:
                self.add_annot(node, toc_ls[i + 1][1], toc_ls[i][2] - 1, toc_ls[i + 1][2] - 1)

    def add_annot(self, node, next_mark, begin, end):
        print(begin, end, node.plaintext, next_mark, self.belongs_to_previous_page)
        page = self.pdf[begin]
        for annot_num in range(self.belongs_to_previous_page, len(list(page.annots(types=[fitz.PDF_ANNOT_HIGHLIGHT])))):
            node.add_child(core=f"P{begin + 1}-{annot_num + 1}")
        self.belongs_to_previous_page = 0

        for page_num in range(begin + 1, end):
            for annot_num in range(len(list(self.pdf[page_num].annots(types=[fitz.PDF_ANNOT_HIGHLIGHT])))):
                node.add_child(core=f"P{page_num + 1}-{annot_num + 1}")

        page = self.pdf[end]
        possible_words = [w for w in page.get_text("words") if w[4] in next_mark]
        d = defaultdict(list)
        for word in possible_words:
            d[round(word[1])].append(word)
        if not d:
            print("NOTFOUND")
            return
        y0 = max(d.values(), key=len)[0][1]
        for annot_num in range(len(annot_ls := list(page.annots(types=[fitz.PDF_ANNOT_HIGHLIGHT])))):
            annot = annot_ls[annot_num]
            if fitz.Quad(annot.vertices[:4]).rect.y0 <= y0:
                node.add_child(core=f"P{end + 1}-{annot_num + 1}")
                self.belongs_to_previous_page += 1


if __name__ == '__main__':
    t = GenerateMM(path_fit_platform(r'E:\学习资料\计算机\参考书\可能会读的书\C++\入门\C++Primer\C++Primer_test.mm'),
                   path_fit_platform(r'E:\学习资料\计算机\参考书\可能会读的书\C++\入门\C++Primer\C++Primer5edCN.pdf'),
                   True)
    t.generate()
