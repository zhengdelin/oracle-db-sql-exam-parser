import os


def mkdirIfNotExists(path):
    os.mkdir(path) if not os.path.exists(path) else None


def isDirEmpty(dirPath):
    files = os.listdir(dirPath)
    return len(files) == 0


def deleteFilesInDir(dirPath, recursive=True):
    try:
        files = os.listdir(dirPath)
        for file in files:
            filePath = os.path.join(dirPath, file)
            if os.path.isfile(filePath):
                os.remove(filePath)
            elif recursive and os.path.isdir(filePath):
                deleteFilesInDir(dirPath, True)
        return True
    except OSError as e:
        print("刪除檔案時發生錯誤：", e)
        return False
