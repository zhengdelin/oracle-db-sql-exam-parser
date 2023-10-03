import os


def mkdirIfNotExists(path):
    os.mkdir(path) if not os.path.exists(path) else None


def deleteFilesInDir(dirPath, recursive=True):
    try:
        files = os.listdir(dirPath)
        for file in files:
            filePath = os.path.join(dirPath, file)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif recursive and os.path.isdir(filePath):
                deleteFilesInDir(dirPath, True)
        print("All files deleted successfully.")
    except OSError:
        print("Error occurred while deleting files.")
