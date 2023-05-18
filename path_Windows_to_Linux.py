import platform

platform = platform.system()
isLinux = platform == "Linux"
isWindows = platform == 'Windows'


def path_Windows_to_Linux(addr, to_Linux=isLinux):
    if not to_Linux:
        return addr
    addr = addr.replace(":", "")
    addr = addr.replace("\\", "/")
    return f"/mnt/{addr}"


def path_Linux_to_Windows(addr, to_Windows=isWindows):
    if not to_Windows:
        return addr
    addr_ls = addr.split('/')
    return f"{addr_ls[2]}:\\" + '\\'.join(addr_ls[3:])


func_dict = {"Linux": path_Windows_to_Linux, "Windows": path_Linux_to_Windows}