# -- coding:utf-8 --
# python路径常用函数 os.path #

import os

#返回目录或者文件名 = os.path.split(path)[1]
os.path.basename(path)

#返回文件目录或者路径的父目录 = os.path.split(path)[0]
os.path.dirname(path)

#判断文件、目录是否存在
os.path.exists(path)

#拼接路径， 以系统分隔符 (os.sep)
os.path.join(path1,path2)

#规范化路径，将反斜杠转为斜杠，字母转为小写
os.path.normcase('c:\Test') #'c:/test' 

#将路径分为一个元组，以最后一个斜杠为分界线，如果最后一个字符为斜杠，那么返回的第2个元素为空
os.path.split('c:/1/')  #('c:/1', '')
os.path.split('c:/1')  #('c:/', '1')
os.path.split('c:/1/1.txt') #('c:/1', '1.txt')

#将路径转换为一个元祖，如果为目录则第二个元素为空，如果文件则第二个元素为文件扩展名
os.path.splitext('c:/1') #('c:/1, '')
os.path.splitext('c:/1/1.txt') #('c:/1', '.txt')

#os.path.walk(path, visit, arg) 
#遍历目录及子目录
#path:待遍历根目录 visit(arg, dirname, names) 遍历目录的函数 dirname目录名，names目录下文件名(也包含目录)字列表
def showfiles(arg, dirname, names):
 print "目录：%s" % dirname
 #os.path.join拼接路径
 #os.path.isfile判断是否为文件 os.path.isdir判断是否为目录
 names=[n for n in names if os.path.isfile(os.path.join(dirname,n))]
 print "目录中文件：%s" % ','.join(names)
os.path.walk('E:/python/walk', showfiles, '')