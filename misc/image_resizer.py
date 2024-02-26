import os
from PIL import Image
from path_cross_platform import path_fit_platform

base = path_fit_platform(r"E:\共享\kdetmp")
dest = path_fit_platform(r"E:\共享\dst")


for image in os.listdir(base):
    img = Image.open(os.path.join(base, image))
    width, height = img.size
    resized = img.resize((int(width * 0.5), int(height * 0.5)))
    resized.save(os.path.join(dest, image))
    print(f"{image} complete!")
