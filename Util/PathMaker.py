import os


def make_path(_tuple):
    path = ""
    for i in _tuple:
        path = os.path.join(path, i)

    return path
