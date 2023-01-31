import platform

isLinux = (platform.system() == "Linux")


def path_Windows_to_Linux(addr, to_Linux=isLinux):
    if not to_Linux:
        return addr
    addr = addr.replace(":", "")
    addr = addr.replace("\\", "/")
    return f"/mnt/{addr}"
