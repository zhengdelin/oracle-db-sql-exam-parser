from module.output import toKeywordDir
ALP = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]

toKeywordDir()


class Keyword:
    question = open("question.txt").read()
    correctAnswer = open("answer.txt").read()
    explanation = open("explanation.txt").read()
    image = r"@@.*?\.jpg@@"
