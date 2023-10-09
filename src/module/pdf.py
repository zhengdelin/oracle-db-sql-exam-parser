import os
import fitz_new as fitz
from module.output import toOutputDir, OUTPUT_DIR, toRootDir


def isAdvertiseImage(width, height, bpc):
    return width == 300 and height == 79 and bpc == 8


def getMaxImageSize(doc: fitz.open):
    maxImgWidth, maxImgHeight, imgCounts = 0, 0, 0
    for page in doc:
        imgInfos = page.get_images(True)
        for imgInfo in imgInfos:
            # print(imgInfo)
            w, h, bpc = imgInfo[2], imgInfo[3], imgInfo[4]
            if (isAdvertiseImage(w, h, bpc)):
                continue

            if (w > maxImgWidth):
                maxImgWidth = w
            if (h > maxImgHeight):
                maxImgHeight = h
            # print(w, h)

            imgCounts += 1
    return (maxImgWidth, maxImgHeight, imgCounts)


__PDF_TO_TXT_FILE_NAME = "parse-image-output-to-txt.txt"
PDF_TO_TXT_FILE_PATH = os.path.join(OUTPUT_DIR, __PDF_TO_TXT_FILE_NAME)

# 由於直接讀取圖片寫入text會導致圖層不同，轉換出來的文字位置會跑掉


def parsePDFImagesThenToTXT(filename: str, imgPrefix=""):
    toRootDir()
    doc = fitz.open(filename)
    toOutputDir()
    txtFile = open(__PDF_TO_TXT_FILE_NAME, "w", encoding="utf-8")

    print()
    print("開始掃描PDF圖片")
    (maxImgWidth, maxImgHeight, imgCountsShouldHave) = getMaxImageSize(doc)
    print(f"掃描到 {imgCountsShouldHave} 張圖片")

    print()
    print("開始解析PDF")
    imgCounts = 0
    for page in doc:
        pageWidth, pageHeight = page.rect.x1, page.rect.y1
        # print(pageWidth, pageHeight)

        # pageNum = page.number
        # print(pageNum+1)

        texts = ""

        # get_images取得的座標，座標中心點在左上，往右表示x座標遞增，往下表示y座標遞增
        # 而get_text時，pdf座標中心在右上角，往左表示y座標遞增，往下表示x座標遞增
        # 因此之前測到的高度要當作寬度使用，寬度當作高度使用(相當於翻轉90度)
        clipRectX = max(pageHeight, maxImgHeight)
        clipRectY = max(pageWidth, maxImgWidth)
        OFFSET = 200
        clipRect = (clipRectX * -1 - OFFSET, clipRectY * -
                    1 - OFFSET, clipRectX + OFFSET, clipRectY + OFFSET)

        pageDict = page.get_text("dict", clip=clipRect)

        # 開始分析dict，block->line->span->text
        for block in pageDict["blocks"]:
            blockType = block["type"]
            isImageBlock = blockType == 1
            # print(block if not isImageBlock else f"img block{imgCounts+1}")
            curBlockTexts = ""
            if (isImageBlock):
                # print(block["bbox"])
                imgData, w, h, bpc = block["image"], block["width"], block["height"], block["bpc"]
                # counter += 1
                # print(counter)
                if (isAdvertiseImage(w, h, bpc)):
                    continue
                imgName = f"{imgPrefix}{imgCounts+1}.jpg"
                img = open(imgName, "wb")
                img.write(imgData)
                img.close()
                imgCounts += 1

                curBlockTexts = f"@@{imgName}@@\n"
            else:
                for line in block["lines"]:
                    # print("---line---")
                    for span in line["spans"]:
                        curBlockTexts += span["text"] + " "
                        # print(span["text"])
                    curBlockTexts += "\n"
                curBlockTexts += "\n"
            # print(curBlockTexts)
            texts += curBlockTexts
        txtFile.write(texts)
    print(
        f"PDF圖片解析完成，應解析 {imgCountsShouldHave} 張圖片，共解析 {imgCounts} 張圖片，已存至 {os.path.join(OUTPUT_DIR, f'{imgPrefix}**.jpg')}"
    )
    txtFile.close()
    print(f"PDF轉換完成，已存至 {PDF_TO_TXT_FILE_PATH}")


def readPDFToTXTTexts():
    toOutputDir()
    f = open(__PDF_TO_TXT_FILE_NAME, "r", encoding='utf-8')
    texts = f.read()
    f.close()
    return texts
