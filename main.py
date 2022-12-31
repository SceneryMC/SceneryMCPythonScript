with open(r"C:\Users\SceneryMC\Source\Repos\assembly\first_window.asm", encoding='utf8') as f:
    lines = f.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].rstrip() + "\n"

with open(r"C:\Users\SceneryMC\Source\Repos\assembly\first_window.asm", 'w', encoding='utf8') as f:
    f.writelines(lines)
