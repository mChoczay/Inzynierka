import glob

path = r"/INZYNIERKA"


def counter():
    iniCounter = len(glob.glob1(path, "*.ini")) - 1
    return iniCounter
