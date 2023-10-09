import os
from util.os import mkdirIfNotExists

__OUTPUT_DIR_NAME = "outputs"
__KEYWORD_DIR_NAME = "keywords"

ROOT_DIR = os.getcwd()
SRC_ROOT_DIR = os.path.join(ROOT_DIR, "src")
OUTPUT_DIR = os.path.join(ROOT_DIR, __OUTPUT_DIR_NAME)
KEYWORD_DIR = os.path.join(ROOT_DIR, __KEYWORD_DIR_NAME)


def toOutputDir():
    mkdirIfNotExists(OUTPUT_DIR)
    os.chdir(OUTPUT_DIR)


def toKeywordDir():
    os.chdir(KEYWORD_DIR)


def toRootDir():
    os.chdir(ROOT_DIR)


def toSrcRootDir():
    os.chdir(SRC_ROOT_DIR)
