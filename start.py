from AI_2048 import AI_2048
from grid import grid

rule = ['Up', 'Right', 'Down', 'Left']
field=[[4,8,32,16],[2,0,4,4],[0,0,0,2],[0,0,0,0]]
# 实例化一个grid生成newgrid，然后把newgrid作为参数实例化AI_search
newgrid = grid(current_grid=field)
ai_2048 = AI_2048(grid=newgrid)
ai_2048_exec_after = ai_2048.getBest()
# 返回来的move是一个0-3的数字，根据规则rule然后转化成方向文字
# //direction   0: up, 1: right, 2: down, 3: left
# direction是英文文字 Up，Right，Down，Left
# ai_2048_exec_after['move']返回来的是一个数字然后根据rule里面的对照关系返回因为字母Up，Right，Down，Left给direction
if 'move' in ai_2048_exec_after:
    print(ai_2048_exec_after['move'])
else:
    print('not exist')
# n = ai_2048_exec_after['move']
# direction = rule[n]
# print(direction)