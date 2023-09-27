import os
from util.os import mkdirIfNotExists

__OUTPUT_DIR_NAME = "outputs"

ROOT_DIR = os.getcwd()
OUTPUT_DIR = f"{ROOT_DIR}\{__OUTPUT_DIR_NAME}"


def toOutputDir():
    mkdirIfNotExists(OUTPUT_DIR)
    os.chdir(OUTPUT_DIR)


def toRootDir():
    os.chdir(ROOT_DIR)
