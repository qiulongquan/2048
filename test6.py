# # 多线程锁的使用
# # coding : uft-8
# __author__ = 'Phtih0n'
# import threading, time
#
# n = 0
# class MyThread(threading.Thread):
#
#     def __init__(self):
#         threading.Thread.__init__(self)
#     def run(self):
#         global n
#         time.sleep(1)
#         if lock.acquire():
#             print ("{},{}".format(n , self.name))
#             n += 1
#             lock.release()
#
#
# if "__main__" == __name__:
#     n = 1
#     ThreadList = []
#     lock = threading.Lock()
#     for i in range(1, 20):
#         t = MyThread()
#         ThreadList.append(t)
#     for t in ThreadList:
#         t.start()
#     for t in ThreadList:
#         t.join()

# -----------------------------------------------------------
# # 多线程锁的使用
# #!/usr/bin/python
# import threading
# i = 0
# i_lock = threading.Lock()
#
# def test():
#     global i
#     i_lock.acquire()
#     try:
#         for x in range(100000):
#             i += 1
#     finally:
#         i_lock.release()
#
# threads = [threading.Thread(target=test) for t in range(10)]
# for t in threads:
#     t.start()
#
# for t in threads:
#     t.join()
#
# assert i == 1000000, i



# if not 0 \
#         and not 0 \
#         and not 0 \
#         and not 0 \
#         and not 0 \
#         and not 0 \
#         and not 0 \
#         and not 0 \
#         and not 0:
#     print("0")
# else:
#     print("1")



# # 数组转换convert
# list=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
# # list_new_sample=[[{'value':0,'marked':True},{'value':0,'marked':True},{'value':0,'marked':True},{'value':0,'marked':True}]
# #         ,[{'value':0,'marked':True},{'value':2,'marked':False},{'value':0,'marked':True},{'value':0,'marked':True}]
# #         ,[{'value':0,'marked':True},{'value':2,'marked':False},{'value':0,'marked':True},{'value':0,'marked':True}]
# #         ,[{'value':0,'marked':True},{'value':2,'marked':False},{'value':0,'marked':True},{'value':0,'marked':True}]]
#
# size=4
# # 先定义一个row ，colum的空2维数组 每个cell里面的值为0
# # 程序中动态定义生成一个2维数组
# list_new = [[0 for col in range(size)] for row in range(size)]
# for x in range(size):
#     for y in range(size):
#         list_new[x][y] = {'value': 0, 'marked': True}
#
#
# for x in range(len(list)):
#     for y in range(len(list[x])):
#         list_new[x][y]['value'] = list[x][y]
#
#
# print(list_new[1][1])
# print(list_new[1][1]['value'])
# print(list_new[1][1]['marked'])
#
# print(list_new[3][1])
# print(list_new[3][1]['value'])
# print(list_new[3][1]['marked'])



# import time
# # 这个时间单位是秒
# a = time.time()
# print ("a时间戳为:", a)
# n = 0
# for i in range(100000):
#    n += 1
# b = time.time()
# print("b时间戳为:", b)
# c = (time.time() - a)*1000
# print("毫秒时间戳为:", c)
# if c > 17:
#     print(">")
# else:
#     print("<")


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

