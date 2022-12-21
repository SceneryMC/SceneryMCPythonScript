new_lines = []
with open(r"C:\Users\SceneryMC\Source\Repos\assembly\first_window.asm") as f:
    lines = f.readlines()
    for line in lines:
        if line == '\n':
            new_lines.append("\n")
            continue
        line = line[:line.find(';')]
        if line != "":
            new_lines.append(f"{line}\n")

with open(r"C:\Users\SceneryMC\Source\Repos\assembly\first_window.asm", 'w') as f:
    f.writelines(new_lines)
