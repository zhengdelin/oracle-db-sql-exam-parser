import zipfile
from module.output import toOutputDir, OUTPUT_DIR
import os

__ZIP_FILE_NAME = "output.zip"


def zipOutputs():
    toOutputDir()
    files = os.listdir()
    try:
        with zipfile.ZipFile(__ZIP_FILE_NAME, mode="w") as zf:
            for f in files:
                zf.write(f)
        print(f"\n壓縮成功，已存至 {os.path.join(OUTPUT_DIR, __ZIP_FILE_NAME)}")
    except Exception as e:
        print("壓縮失敗，Error:", e)
