import os
import platform

platform = platform.system()


def deduce_old_platform(path: str) -> str:
    return 'Linux' if path.startswith('/mnt') else 'Windows'


def path_fit_platform(path: str, dst_platform: str = platform) -> str:
    old_platform = deduce_old_platform(path)
    if dst_platform != old_platform:
        return path_Linux_to_Windows(path) if dst_platform == 'Windows' else path_Windows_to_Linux(path)
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