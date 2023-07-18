import fitz
import freeplane
from path_cross_platform import *
from pdf_page_and_annot_linker import generate_command

files = {

}
template_address = path_fit_platform(
    r"C:\Users\SceneryMC\AppData\Roaming\Freeplane\1.10.x\templates\xmind2021_default.mm")

class GenerateMM:
    def __init__(self, mm_path, pdf_path):
        self.pdf_path = pdf_path
        self.mm_path = mm_path
        doc = fitz.open(path_fit_platform(self.pdf_path))
        self.toc = doc.get_toc()

    def generate(self):
        mm = freeplane.Mindmap(template_address)
        prop = mm.rootnode._node.find('.//properties')
        prop.set("associatedTemplateLocation", 'template:/xmind2021_default.mm')
        self.add_node(mm.rootnode)
        mm.save(self.mm_path, encoding='utf-8')

    def add_node(self, root):
        stack = [root]
        toc_ls = self.toc + [[1]]
        for i in range(len(self.toc)):
            node = stack[-1].add_child()
            node.plaintext = self.toc[i][1]
            node.hyperlink = f"execute:_{generate_command(self.pdf_path, self.toc[i][2])}"
            if (diff := toc_ls[i][0] - toc_ls[i + 1][0]) > 0:
                stack = stack[:-diff]
            elif toc_ls[i][0] < toc_ls[i + 1][0]:
                stack.append(node)


for file in files.values():
    GenerateMM(path_fit_platform(file[0]), path_fit_platform(file[1])).generate()
