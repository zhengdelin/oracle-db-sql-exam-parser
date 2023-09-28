from module.constants import ALP, Keyword
import re
from module.pdf import readPDFToTXTTexts
from module.output import toOutputDir, toRootDir, OUTPUT_DIR


def getChoiceTypeRegex(type: str): return rf"(?=(\n|\b)){type}\.(\t|\s)?"


class KeywordReplacer:
    def __init__(self, regex, addNewlineAfterText=False) -> None:
        self.keyword = regex
        self.addNewlineAfterText = addNewlineAfterText

    def handler(self, matches: re.Match):
        text = matches.group(0)
        return f"\n{text}" + ("\n" if self.addNewlineAfterText else "")


KEYWORDS_TO_REPLACE = [
    KeywordReplacer(Keyword.question, True),
    KeywordReplacer(Keyword.correctAnswer),
    KeywordReplacer(Keyword.explanation, True),
    KeywordReplacer(Keyword.image, True),
] + [KeywordReplacer(getChoiceTypeRegex(i)) for i in ALP]

toRootDir()
keywordsToDeleteFile = open("keywords/to-delete.txt")
KEYWORDS_TO_DELETE = keywordsToDeleteFile.read().split("\n")


__KEYWORDS_PRE_HANDLED_FILE_NAME = "keywords-pre-handled.txt"


def handleRawTXTKeywords():
    texts = readPDFToTXTTexts()
    for keyword in KEYWORDS_TO_DELETE:
        texts = re.sub(keyword, "", texts)
    # print(QUESTION_REGEX)
    for keywordReplacer in KEYWORDS_TO_REPLACE:
        # print(keyword, type(keyword))
        texts = re.sub(keywordReplacer.keyword, keywordReplacer.handler, texts)

    toOutputDir()
    f = open(__KEYWORDS_PRE_HANDLED_FILE_NAME, "w")
    f.write(texts)
    f.close()

    print(f"\n關鍵字替換完成，已存至 {OUTPUT_DIR}\{__KEYWORDS_PRE_HANDLED_FILE_NAME}")

    return texts
