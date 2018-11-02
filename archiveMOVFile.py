

import os
import sys
import io
import re, shutil, time
import hachoir
from hachoir import metadata
from hachoir import parser
from sys import exit

from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

class ReadFailException(Exception):
    pass

def getOriginalDate(filename: object) -> object:
    parser=createParser(filename)  # 解析文件
    if not parser:
        print("Unable to parse file - {}\n".format(filename))
        return False
    with parser:
        try:
            metadata=extractMetadata(parser)  # 获取文件的metadata
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            metadata=None

    if not metadata:
        print("Unable to extract metadata")

    if metadata:
        try:
            t=metadata.exportPlaintext(line_prefix="")[4][15:25]  # 截取建立日期
            return str(t).replace("-", ".")
        except:
            pass

def classifyPictures(sourceDir, targetDir):
    for root, dirs, files in os.walk(sourceDir, True):
        # dirs[:] = []
        for filename in files:
            filename=os.path.join(root, filename)
            #print(myfilename)
            f, e=os.path.splitext(filename)
            if e.lower() not in ('.mov','.MOV'):
                continue
            filetype=e.lower().strip('\.')
            info="文件名: " + filename + " "
            t=""

            try:
                t=getOriginalDate(filename)
            except:
                continue

            info=info + "拍摄时间：" + t + " "
            dst=f'{targetDir}/{t}/{filetype}'
            # print(dst)

            # 建立目录
            if not os.path.exists(dst):
                os.makedirs(dst)

            print(info, dst)
            shutil.copy2(filename, dst)
            os.remove(filename)

if __name__ == "__main__":
    #sourceDir='C:/Users/suzhan/Desktop/movtest1'  # 文件复制源路径
    #targetDir='C:/Users/suzhan/Desktop/mov-d'  # 文件复制目标路径
    sourceDir='D:/backup-to-google'  # 文件复制源路径
    targetDir='D:/new-phone/'  # 文件复制目标路径
    classifyPictures(sourceDir, targetDir)
