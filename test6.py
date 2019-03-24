import time
# 这个时间单位是秒
a = time.time()
print ("a时间戳为:", a)
n = 0
for i in range(100000):
   n += 1
b = time.time()
print("b时间戳为:", b)
c = (time.time() - a)*1000
print("毫秒时间戳为:", c)
if c > 17:
    print(">")
else:
    print("<")
# a={'a1':[1,2],'b1':[3,4]}
# print(a['a1'][0])
#
# list=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
# print(list[0][3])
# list[0][3]=111
# print(list[0][3])

#import math
# a=[1,2,5,7]
# b=[10,1,3,4,56]
# print(max(max(a),max(b)))

# 复合字典
# scores1 = {2: [], 4: []}
# scores = {2: [[2,[0,2]],[5,[1,3]],[7,[0,4]]], 4: [[21,[10,21]],[51,[2,31]],[71,[0,41]]]}
# scores[2][1][0]=100
# for value in scores:
#     for i in range(len(scores[value])):
#         print(scores[value][i][0])
#         print(scores[value][i][1])
#
# print(scores[value][i][1][1])


# scores = {2: [], 4: []}
# for value in scores:
#     print(value)


# cells = [[2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2], [2, 2, 2, 2]]
# scores = {2: [], 4: []}
# for value in scores:
#     for i in cells:
#         cell = cells[i]

