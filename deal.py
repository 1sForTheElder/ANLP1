# -*- coding: utf-8 -*-
import _File
import re


# b='#'
# f=open('test1.txt','w' 'r')    # r只读，w可写，a追加
# for i in range(0,2):
#     g = open("test.txt")
#     for line in g:
#         line = b + b + line[:-1] + b
#         f.write(line)
# f.close()
#
# gg = open("f.txt").read()
# print gg
#
# # file=open("test.txt")
# #
# # for line in file:
# #     line = b+b + line[:-1] + b
# #     # print (line)
#
import re
temp = "想做/ 兼_职/学生_/ 的 、加,我Q：  1 5.  8# 0. ！！？？  8 6 。0.  2。 3     有,惊,喜,哦"
temp = temp.decode("utf8")
string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[^+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"),temp)
print string