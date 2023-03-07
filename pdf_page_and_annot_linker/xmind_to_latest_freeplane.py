import xmindparser
import freeplane
import shutil
import os

indent = '    '
styles = {"minorTopic": "重要", "importantTopic": "极其重要", 'topic': "", None: ""}
xmind_basis = '/home/scenerymc/.config/XMind/Electron v3/vana/workbooks/'
xmind_image_path = os.path.join(xmind_basis, os.listdir(xmind_basis)[0], 'resources')

xmind_path = '/mnt/E/学习资料/计算机/参考书/可能会读的书/算法/算法导论/整理/15第十五章：动态规划.xmind'
freeplane_path = '/mnt/E/学习资料/计算机/参考书/可能会读的书/算法/算法导论/整理/CLRS.mm'

freeplane_image_path, mm_filename = os.path.split(freeplane_path)
mm_filename = mm_filename[:-3]
freeplane_image_folder = f'{mm_filename}_files'
freeplane_image_path = f"{freeplane_image_path}/{freeplane_image_folder}"
if not os.path.exists(freeplane_image_path):
    os.mkdir(freeplane_image_path)


def processing_demo(object, layer):
    if isinstance(object, list):
        for item in object:
            processing_demo(item, layer)
    elif isinstance(object, dict):
        for key, value in object.items() or {}.items():
            if isinstance(value, (str, int, float)):
                print(f"{indent * layer}{key}:{value}")
            else:
                print(f"{indent * layer}{key}:")
                processing_demo(value, layer + 1)


def json_to_freeplane(object, node):
    if isinstance(object, list):
        for item in object:
            json_to_freeplane(item, node)
    elif isinstance(object, dict):
        text = object['title']
        no_image = False
        if 'extensions' in object \
                and object['extensions'] \
                and object['extensions'][0]['provider'] == "org.xmind.ui.mathJax":
            latex = object['extensions'][0]['content']['content']
            latex = latex.replace(r"\begin{align}", "")
            latex = latex.replace(r"\end{align}", "")
            latex = latex.replace("&", "")
            text = f"\\latex\n${latex}$"
            no_image = True
            print(text)
        style = styles[object.get('class', None)]
        new_node = node.add_child(core=text, style=style)
        if not no_image and 'image' in object:
            image = object["image"]["src"].split("/")[-1]
            shutil.copy(f'{xmind_image_path}/{image}', f"{freeplane_image_path}/")
            new_node.set_image(link=f'{freeplane_image_folder}/{image}', size=0.4)
        if 'children' in object:
            json_to_freeplane(object['children']['attached'], new_node)


j = xmindparser.get_xmind_zen_builtin_json(xmind_path)[0]['rootTopic']
# print(j)
# processing_demo(j, 0)

mindmap = freeplane.Mindmap(freeplane_path)
json_to_freeplane(j, mindmap.rootnode)
mindmap.save(freeplane_path)
