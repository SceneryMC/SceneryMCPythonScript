import os
import platform

platform = platform.system()


def deduce_old_path_sep(path: str) -> str:
    return '/' if path.startswith('/mnt') else '\\'


def path_fit_platform(path: str) -> str:
    old_path_sep = deduce_old_path_sep(path)
    if os.sep != old_path_sep:
        return path_Linux_to_Windows(path) if os.sep == '\\' else path_Windows_to_Linux(path)
    return path


def path_Windows_to_Linux(path):
    path = path.replace(":", "").replace("\\", "/")
    return f"/mnt/{path}"


def path_Linux_to_Windows(path):
    path_ls = path.split('/')
    return f"{path_ls[2]}:\\" + '\\'.join(path_ls[3:])


def platform_not_match(path):
    return (platform == "Linux") ^ path.startswith("/mnt")


func_dict = {"Linux": path_Windows_to_Linux, "Windows": path_Linux_to_Windows}