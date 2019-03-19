#-*- coding:utf-8 -*-
import random


field = [[0 for i in range(4)] for j in range(4)]
print(field)
f=open("test.txt","a+")

#  4*4的数组里面的数字变换成文字列然后写入文件
row_str = ''
for row in field:
    for i in range(len(row)):
        maped_num = map(str, row)  # 格納される数値を文字列にする
        row_str = ','.join(maped_num)
    f.write(row_str+"\n")
f.close()

# num = [1, 2, 3]
# maped_num = map(str, num)  # 格納される数値を文字列にする
# mojiretsu = ','.join(maped_num)
#
# print(mojiretsu)