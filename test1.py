#-*- coding:utf-8 -*-
import random
import six
from random import randrange, choice  # generate and place new tile

def init1():
    print("1")
    return 'Game'

def game():
    print("2")
    return 'Win'

def Win():
    print("3")
    return 'Gameover'

def Gameover():
    print("4")
    return 'Exit'




new_element = 4 if random.randrange(100) > 50 else 2
print (new_element)

row=4

# new_row = [i for i in row if i != 0]
# # new_row += [0 for i in range(len(row) - len(new_row))]
# print (new_row)

field = [[0 for i in range(4)] for j in range(4)]
print (field)

print([(i,j) for i in range(4) for j in range(4) if field[i][j] == 0])
print(random.choice([(i,j) for i in range(4) for j in range(4) if field[i][j] == 0]))

print("="*80)
# 状态机 方法调用实例 通过字典获取方法名字然后调用并取回下一个要调用的方法的名字然后再调用下一个方法。
state_actions = {
    'Init1': init1,
    'Win': Win,
    'Gameover': Gameover,
    'Game': game
}

state = 'Init1'

# 状态机开始循环
while state != 'Exit':
    # print(state_actions[state])
    state = state_actions[state]()
    print("state=",state)
print("exit")


print("="*80)
# 键盘按键对应的操作
letter_codes = [ord(ch) for ch in 'WASDRQwasdrq']
actions = ['Up', 'Left', 'Down', 'Right', 'Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))
print(actions_dict)

# char = '83'
# if char in actions_dict:
#     print("ok")
#
# for ch in actions_dict:
#     # int和bytes的转换用six类库把 int转成bytes得到b，然后把b转换成string。
#     b = six.int2byte(ch)
#     str1 = str(b, 'utf-8')
#     print(str1)
#     if 'W' == str1:
#         print('我是W')
#
# # 字典里面的key是可以in操作的，可以指定一个字符在字典里面查找是否存在。
# a={'A':'1','B':'2','C':'3','D':'4'}
# aa='B'
# print(aa in a)

actions1 = ['Up', 'Left', 'Down', 'Right']
direction = choice(actions1)
print("方向操作:", direction)
