import os
from util.os import mkdirIfNotExists, deleteFilesInDir

__OUTPUT_DIR_NAME = "outputs"

ROOT_DIR = os.getcwd()
SRC_ROOT_DIR = os.path.join(ROOT_DIR, "src")

OUTPUT_DIR = os.path.join(ROOT_DIR, __OUTPUT_DIR_NAME)


def toOutputDir():
    mkdirIfNotExists(OUTPUT_DIR)
    os.chdir(OUTPUT_DIR)


def clearOutputDir():
    if (os.path.exists(OUTPUT_DIR)):
        deleteFilesInDir(OUTPUT_DIR)


def toRootDir():
    os.chdir(ROOT_DIR)


def toSrcRootDir():
    os.chdir(SRC_ROOT_DIR)
