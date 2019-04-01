count=[]
a=[1,2,3,4,4,5]
for i in range(3):
    count.append(len(a))
print(count[0])



# import traceback
#
#
# def a():
#     print("a")
#
# def b():
#     print("b")
#
# def c():
#     raise Exception("Data Source から取得件数は取り漏れが発生しましたから、全体バッチが中止となります.")
#     # raise Exception("Data Source Retrieval API Failed.")
#     print("c")
#
# def d():
#     print("d")
#
# def e():
#     print("e")
#
# message = ""
# while True:
#     try:
#         a()
#         b()
#         c()
#         d()
#         e()
#
#     except Exception as ex:
#         message += " failed.\n"
#         message += "Error Type: {}\n".format(type(ex))
#         message += "Error Message: {}\n".format(ex)
#         message += traceback.format_exc()
#         print("Error Type: {}".format(type(ex)))
#         print("Error Message: {}".format(ex))
#         print(traceback.format_exc())
#         break
#     else:
#         message += " succeed.\n"
#         print(" succeed.")