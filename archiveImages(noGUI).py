# -*- coding: gbk -*-

#
# 所指定目录下的所有视频,图片文件按日期归档
#

import os
import exifread
import re, shutil, time
import hachoir
import filecmp
import hashlib
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata


def getOriginalDate(filename):
    """
    处理'.jpg', '.png', '.mp4', '.nef', '.3gp', '.flv', '.mkv'文件.读出建立日期
    """


    try:
        fd = open(filename, 'rb')
    except:
        raise ReadFailException("unopen file[%s]\n" % filename)
        data = exifread.process_file(fd)
    
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            return str(t).replace(":", ".")[:10]
        except:
            pass
            state = os.stat(filename)
            return time.strftime("%Y.%m.%d", time.localtime(state[-2]))


def getOriginalDateMOV(filename):
    """
    单独处理mov视频文件,读出建立日期
    """
    parser = createParser(filename)  # 解析文件

    if not parser:
        print("Unable to parse file - {}\n".format(filename))
        print(filename)
        return False
    with parser:
        try:
            metadata = extractMetadata(parser)  # 获取文件的metadata
        except Exception as err:
            print("Metadata extraction error: %s" % err)
            metadata = None

    if not metadata:
        print("Unable to extract metadata")

    if metadata:
        try:
            t = metadata.exportPlaintext(line_prefix="")[4][15:25]  # 截取建立日期
        return str(t).replace("-", ".")
        except:
        pass


def calculate_hashes(self, filename):
    """
    得出文件的MD5,sha1码,用于对比文件
    """
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    with open(filename, "rb") as f:
        data = f.read()
    md5_returned = hashlib.md5(data).hexdigest()
    sha1_returned = hashlib.sha1(data).hexdigest()
    return md5_returned, sha1_returned


def calculate_filesize(self, filename):
    """
    得出文件的大小,用于对比文件
    """
    with open(filename, "rb") as f:
        filesize_returned = os.path.getsize(filename)
    return filesize_returned


def classifyPictures(sPath, dPath):
    """
    复制文件到新的文件夹,删除原文件
    """
    count = 0

    for root, dirs, files in os.walk(sPath, True):
        # dirs[:] = []
        for filename in files:
            count = count + 1
            filename = os.path.join(root, filename)
            f, e = os.path.splitext(filename)
            
        if e.lower() not in ('.jpg', '.png', '.nef', '.mp4', '.3gp', '.flv', '.mkv', '.mov'):
            continue
            filetype = e.lower().strip('\.')
            info = "文件名: " + filename + " "
            t = ""
        try:
            if filetype == "mov":
                t = getOriginalDateMOV(filename)
        else:
        t = getOriginalDate(filename)
        except Exception as e:
        print(e)
        continue
        info = info + "拍摄时间：" + t + " "
        tyear = t[0:4]
        dst = f'{dPath}{tyear}/{t}/{filetype}'

    
    if not os.path.exists(dst):
        os.makedirs(dst)
    
        dstfilename = os.path.basename(filename)
        dstfile = f'{dst}/{dstfilename}'
    
    # 如果目标有同名文件,使用md5对比,一样不作处理,不一样变更文件名复制
    if os.path.exists(dstfile):
        if self.calculate_hashes(dstfile) == self.calculate_hashes(archFilename) and self.calculate_filesize(
                dstfile) == self.calculate_filesize(archFilename):
            print('处理文件:', count, dstfilename, "已存在, 不作复制")
        os.remove(filename)
        else:
        newfilename = f'{f}{"_"}{str(count)}{e}'
        shutil.move(filename, newfilename)
        shutil.copy2(newfilename, dst, follow_symlinks=True)
        os.remove(newfilename)
        print('处理文件:', count, dstfilename, "已存在,变更文件名", newfilename, "复制")
        else:
        shutil.copy2(filename, dst, follow_symlinks=True)
        os.remove(filename)
        print('处理文件:', count, info, '复制到:', dst)
        
        print('已经处理文件数:', count)


def cel(path):
    """
    删除空文件及空文件夹
    """

    for root, dirs, files in os.walk(sPath, True):
        for file in files:
            myfile = os.path.join(root, file)
            
    if os.path.getsize(myfile) == 0:
        os.remove(myfile)
        print('清理空文件:', myfile)
    
    for dir in dirs:
        mydir = os.path.join(root, dir)
        
    if not os.listdir(mydir):
        shutil.rmtree(mydir)
        # os.rmdir(mydir)
        print('清理空文件夹:', mydir)

if __name__ == "__main__":
    sPath = "D:/sPath/"
    dPath = "D:/dPath/"
    classifyPictures(sPath, dPath)
    cel(sPath)
