import os
import shutil

directories = os.listdir('.')
directories.remove('main.py')
directories.remove('start.bat')
for directory in directories:
    sub_dirs = os.listdir(f'./{directory}')
    for sub_dir in sub_dirs:
        files = os.listdir(f'./{directory}/{sub_dir}')
        for file in files:
            shutil.copy(f'./{directory}/{sub_dir}/{file}', f'./{directory}')
        shutil.rmtree(f'./{directory}/{sub_dir}')
