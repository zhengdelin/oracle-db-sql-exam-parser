import re
import util.array as array
from module.constants import ALP, Keyword
import module.preHandler as preHandler


def getFindChoiceTypeFunc(
    type: str): return lambda x: x.startswith(f"{type}.")


def getNextChoiceType(type: str): return ALP[ALP.index(type) + 1]


def getChoice(arr: list, index: int, type: str, nextType: str):
    nextTypeIndex = array.findIndex(arr, getFindChoiceTypeFunc(nextType))
    # print("getChoice", arr, type ,nextType, index, nextTypeIndex)
    textList = arr[index:] if nextTypeIndex == None else arr[index:nextTypeIndex]
    text = "\n".join(filter(lambda x: x.strip(), textList))
    return re.sub(preHandler.getChoiceTypeRegex(type), "", text).strip()


def getChoices(arr: list, type=ALP[0], results: list = list()) -> list:
    # print("getChoices", arr, type)
    index = array.findIndex(arr, getFindChoiceTypeFunc(type))
    if (index == None):
        return results

    nextType = getNextChoiceType(type)
    result = {
        "type": type,
        "text": getChoice(arr, index, type, nextType)
    }
    results.append(result)
    # print(result, type, nextType)
    return getChoices(arr[index+1:], nextType, results)


def getSubject(arr: list):
    firstChoiceIndex = array.findIndex(arr, getFindChoiceTypeFunc(ALP[0]))
    return "\n".join(arr[1:firstChoiceIndex]).strip()


def parseAns(arr: list):
    ansIndex = array.findIndex(
        arr, lambda x: x.startswith(Keyword.correctAnswer))
    ans = ",".join(arr[ansIndex].replace(Keyword.correctAnswer,  "").replace(
        "Section: (none) Explanation", "").strip())
    # print(ans)
    ansType = "單選題" if len(ans) == 1 else "複選題"
    explanationIndex = array.findIndex(
        arr, lambda x: x.startswith(Keyword.explanation))
    explanation = ""
    if (explanationIndex):
        explanation = re.sub(r"(Reference|Explanation)s?:",
                             "", "\n".join(arr[explanationIndex+1:]), 1)

    return (
        arr[:ansIndex],
        ans,
        ansType,
        explanation
    )
