import re
import os
import module.examParser as parser
from module.excel import exportToExcel
from module.preHandler import handleRawTXTKeywords
from module.constants import Keyword
from module.pdf import parsePDFImagesThenToTXT
from module.output import toRootDir, toOutputDir, clearOutputDir


def isPDFFile(name: str):
    return name.endswith(".pdf")


def findPDFFile():
    print("開始搜尋pdf檔案...")
    toRootDir()
    files = os.listdir()
    for f in files:
        if (isPDFFile(f)):
            return f
    return None


_pdfFileName = findPDFFile()

fileName = input(
    f"目前使用{_pdfFileName}，輸入檔名以選擇其他檔案(PDF):" if (_pdfFileName != None) else "未搜尋到PDF檔，請輸入檔名：") or _pdfFileName

if (not isPDFFile(fileName)):
    print("檔案必須為pdf檔")
    quit()

imgPrefix = input("請輸入圖片前綴(如:1Z0071-6-):")

toOutputDir()
clearOutputDir()
toRootDir()

try:
    parsePDFImagesThenToTXT(fileName, imgPrefix)
except Exception as e:
    print(e)
    quit()
handledTexts = handleRawTXTKeywords()


splittedTexts = re.split(rf'\b(?={Keyword.question})', handledTexts)
results = []
errorNums = []
# print(splittedTexts)
for i in range(1, len(splittedTexts)):
    curQ = splittedTexts[i].split("\n")
    name = curQ[0]
    qNum = re.search(r"\d+", name).group(0)
    try:
        subject = parser.getSubject(curQ)
        (curQ, ans, ansType, explanation) = parser.parseAns(curQ)
        choices = parser.getChoices(curQ, results=[])
        # print(curQ)
        # print(choices)
        # print("curQ:", name)
        # print("subject:", subject)
        # print("ans, explanation:",ans,ansType, explanation)
        # for i in choices:
        #     print(i['type'],".", i['text'])
        # print("----------")

        results.append({
            "num": qNum,
            "name": name,
            "ansType": ansType,
            "subject": subject,
            "difficulty": "中",
            "ans": ans,
            "explanation": explanation,
            "choices": choices
        })
    except Exception as e:
        errorNums.append(qNum)
        print(f"Error happened in {name}:{e}")


print(f"\n{len(results)} questions has been parsed.")
if len(errorNums) > 0:
    print(f"Errors happened in {', '.join(errorNums)} questions.")


curQNum = 0


def printQuestions(*nums: int):
    global curQNum
    curQNum = max(nums)
    for num in nums:
        try:
            q = results[num - 1]
            print(q['name'])
            print(q['subject'])
            for choice in q['choices']:
                print(f"{choice['type']}.")
                print(choice['text'])
            print(f"ans:{q['ans']}")
            print(f"explanation:{q['explanation']}\n")
        except IndexError:
            print(f"Invalid number {num}")


def clearConsole(): os.system("cls")


while (True):
    try:
        inp = input("""-----------------------------
輸入數字以印出分析結果(以逗點(,)隔開)
按下Enter以印出下一題
輸入e以輸出至Excel並壓縮成zip檔
輸入q離開
input:""")
        if (inp == "q" or inp == "Q"):
            break
        elif (inp == "e" or inp == "E"):
            exportToExcel(results)
        elif (inp == ''):
            clearConsole()
            if (curQNum >= len(results)):
                print("No more questions.")
                continue
            printQuestions(curQNum+1)
        else:
            clearConsole()
            printQuestions(*[int(x) for x in inp.split(",")])

    except KeyboardInterrupt:
        break
    except PermissionError as e:
        print(e)
        print("Please close the file or check the permission.")
    except Exception as e:
        print("Error!", e)
