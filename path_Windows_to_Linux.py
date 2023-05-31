import platform

platform = platform.system()
isLinux = platform == "Linux"
isWindows = platform == 'Windows'


def path_Windows_to_Linux(path, to_Linux=isLinux):
    if not to_Linux:
        return path
    path = path.replace(":", "")
    path = path.replace("\\", "/")
    return f"/mnt/{path}"


def path_Linux_to_Windows(path, to_Windows=isWindows):
    if not to_Windows:
        return path
    path_ls = path.split('/')
    return f"{path_ls[2]}:\\" + '\\'.join(path_ls[3:])


def unmatch_platform(path):
    return isLinux ^ path.startswith("/mnt")


func_dict = {"Linux": path_Windows_to_Linux, "Windows": path_Linux_to_Windows}