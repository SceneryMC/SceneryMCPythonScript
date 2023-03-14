import xmindparser
import freeplane
from zipfile import ZipFile
import os

indent = ' ' * 4
styles = {"minorTopic": "重要", "importantTopic": "极其重要", 'topic': "", None: ""}

xmind_folder_path = ''
freeplane_parent = ''
mm_name = ''

xmind_file_paths = [f"{xmind_folder_path}/{x}" for x in os.listdir(xmind_folder_path) if x.endswith('.xmind')]
mm_path = f"{freeplane_parent}/{mm_name}.mm"
freeplane_image_folder = f'{mm_name}_files'
freeplane_image_path = f"{freeplane_parent}/{freeplane_image_folder}"
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
        ignore_image = False
        if 'extensions' in object \
                and object['extensions'] \
                and object['extensions'][0]['provider'] == "org.xmind.ui.mathJax":
            latex = object['extensions'][0]['content']['content']
            latex = latex.replace(r"\begin{align}", "")
            latex = latex.replace(r"\end{align}", "")
            latex = latex.replace("&", "")
            text = f"\\latex\n${latex}$\n"
            ignore_image = True
            print(text)
        style = styles[object.get('class', None)]
        new_node = node.add_child(core=text, style=style)
        if not ignore_image and 'image' in object:
            img_name = object["image"]["src"].split("/")[-1]
            img_byte = xmind_zip.open(f"resources/{img_name}").read()
            img_path = f"{freeplane_image_path}/{img_name}"
            with open(img_path, 'wb') as f:
                f.write(img_byte)
            new_node.set_image(link=img_path, size=0.6)
        if 'children' in object:
            json_to_freeplane(object['children']['attached'], new_node)


for xmind_file_path in xmind_file_paths:
    xmind_zip = ZipFile(xmind_file_path)
    j = xmindparser.get_xmind_zen_builtin_json(xmind_file_path)[0]['rootTopic']
    # print(j)
    # processing_demo(j, 0)

    mindmap = freeplane.Mindmap(mm_path)
    json_to_freeplane(j, mindmap.rootnode)
    mindmap.save(mm_path)
