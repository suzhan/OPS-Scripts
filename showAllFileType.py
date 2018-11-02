

# coding: utf8
import fnmatch
import os
import pathlib

matches = []
for root, dirnames, filenames in os.walk('C:/Users/suzhan/Desktop/test2'):    #编历目录列出所有文件放入matches
    for filename in fnmatch.filter(filenames, '*.*'):
        matches.append(os.path.join(root, filename))

filetype = []
for i in matches:
    filetype.append((pathlib.Path(i).suffix))     #取出文件类型
filetype = map(str.lower,filetype)   #转换为小写
filetype = list(set(filetype))       #去掉重复值
print(filetype)
