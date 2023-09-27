import os


def mkdirIfNotExists(path):
    os.mkdir(path) if not os.path.exists(path) else None
