# -*- coding:utf-8 -*-

import curses
import sqlite3
import time
from contextlib import closing
from random import randrange, choice  # generate and place new tile
from collections import defaultdict
from AI_2048 import AI_2048
from grid import grid

letter_codes = [ord(ch) for ch in 'RQrq']
actions = ['Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))
actions1 = ['Up', 'Left', 'Down', 'Right']
# 步数 当前是策略的第几步
step = 1
# 当前的对战id号
battle_id = 0
# 当次操作的方向
direction = ''
# 移动前的field状态存储
digital_set_before = ''
# 移动后的field状态存储
digital_set_after = ''

# 链接sqlite3数据库
dbname = 'operation.sqlite3'
conn = sqlite3.connect(dbname)
c = conn.cursor()


# 操作数据和每个方格的数字信息写入文件
f = open('operation_log.txt', 'a+')


def write_file(height='', width='', win='', field=''):
    header = "height={}   width={}    win={}".format(height, width, win)
    f.write(header + "\n")
    #  4*4的数组里面的数字变换成文字列然后写入文件
    f.write("\n")
    row_str = ''
    for row in field:
        for i in range(len(row)):
            maped_num = map(str, row)  # 格納される数値を文字列にする
            row_str = ','.join(maped_num)
        f.write(row_str + "\n")
    f.write("\n"+"="*60+"\n")


# 操作数据和每个方格的数字信息写入文件数据库sqlite3  name为 operation.sqlite3
def write_file_to_operation_insert(battle_id, step=0, new_element=2, coordinate='0,0'):
    sql = 'insert into operation (' \
          'battle_id,' \
          'step,' \
          'new_digital,' \
          'coordinate' \
          ') values (?,?,?,?)'
    record = (battle_id, step, new_element, coordinate)
    c.execute(sql, record)
    conn.commit()


# 更新数据到operation表
def write_file_to_operation_update(battle_id, step=0, direction='', digital_set_before='', digital_set_after=''):
    sql='update operation ' \
        'set ' \
        'Direction=?,' \
        'digital_set_before=?,' \
        'digital_set_after=? ' \
        'where ' \
        'battle_id=? ' \
        'and ' \
        'step=?'
    record = (direction, digital_set_before, digital_set_after, battle_id, step)
    c.execute(sql, record)
    conn.commit()


def write_file_to_record(battle_id=0, ver='', score=0, win_score=2048, width='4', height='4', result=''):
    sql = 'insert into record (' \
          'battle_id,' \
          'ver,' \
          'score,' \
          'win_score,' \
          'width,' \
          'height,' \
          'result' \
          ') values (?,?,?,?,?,?,?)'
    record = (battle_id, ver, score, win_score, width, height, result)
    c.execute(sql, record)
    conn.commit()


# 更新record表中的信息
def write_file_to_record_update(battle_id,score,result):
    sql='update record ' \
        'set ' \
        'score=?,' \
        'result=?' \
        'where ' \
        'battle_id=? '
    record = (score, result, battle_id)
    c.execute(sql, record)
    conn.commit()

# 获取得分最多的时候的分数
def get_highscore():
    sql = 'select max(score) from record;'
    highscore = c.execute(sql).fetchall()[0][0]
    if highscore is None or highscore == '':
        highscore = 0
    return highscore

def get_new_battle_id():
    sql = 'select max(battle_id) as max from record;'
    battle_id = c.execute(sql).fetchall()[0][0]
    if battle_id is None:
        battle_id = 1
    else:
        battle_id = battle_id + 1
    return battle_id

def get_current_battle_id():
    sql = 'select max(battle_id) as max from record;'
    battle_id = c.execute(sql).fetchall()[0][0]
    if battle_id is None:
        battle_id = 0
    return battle_id

def get_field_to_str(field):
    row_str = ''
    row_str_all = ''
    for row in field:
        for i in range(len(row)):
            maped_num = map(str, row)  # 格納される数値を文字列にする
            row_str = ','.join(maped_num)
        row_str_all += " "+row_str
    return row_str_all


# 键盘值的获取，如果不在actions_dict里面就继续监听按键，如果在actions_dict里面就返回对应的操作。
def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def get_machine_direction(field):
    # direction=choice(actions1)
    rule = ['Up', 'Right', 'Down', 'Left']
    print(rule)
    # 实例化一个grid生成newgrid，然后把newgrid作为参数实例化AI_search
    newgrid = grid(current_grid=field)
    ai_2048 = AI_2048(grid=newgrid)
    ai_2048_exec_after = ai_2048.getBest()
    # 返回来的move是一个0-3的数字，根据规则rule然后转化成方向文字
    # //direction   0: up, 1: right, 2: down, 3: left
    # direction是英文文字 Up，Right，Down，Left
    # ai_2048_exec_after['move']返回来的是一个数字然后根据rule里面的对照关系返回因为字母Up，Right，Down，Left给direction
    n = ai_2048_exec_after['move']
    direction = rule[n]
    # print("方向操作:",direction)
    return direction

def transpose(field):
    return [list(row) for row in zip(*field)]

def invert(field):
    return [row[::-1] for row in field]

class GameField(object):
    def __init__(self, height=4, width=4, win=2048):
        write_file(height=4, width=4, win=2048)
        self.height = height
        self.width = width
        self.win_value = win
        self.score = 0
        self.highscore = 0
        self.reset()

    def reset(self):
        self.highscore = get_highscore()
        self.score = 0
        global step
        step = 1
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        # 获取的初期field的数值写入文件和数据库
        battle_id = get_new_battle_id()
        write_file(height=str(self.height), width=str(self.width), win='2048', field=self.field)
        write_file_to_record(battle_id, ver='1.0', win_score=2048, width=str(self.width), height=str(self.height))

        self.spawn()
        self.spawn()

    def move(self, direction):
        def move_row_left(row):
            def tighten(row): # squeese non-zero elements together
                new_row = [i for i in row if i != 0]
                new_row += [0 for i in range(len(row) - len(new_row))]
                return new_row

            def merge(row):
                pair = False
                new_row = []
                for i in range(len(row)):
                    if pair:
                        new_row.append(2 * row[i])
                        self.score += 2 * row[i]
                        pair = False
                    else:
                        if i + 1 < len(row) and row[i] == row[i + 1]:
                            pair = True
                            new_row.append(0)
                        else:
                            new_row.append(row[i])
                assert len(new_row) == len(row)
                return new_row
            return tighten(merge(tighten(row)))

        moves = {}
        moves['Left'] = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up'] = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down'] = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()

                # 获取执行移动后的field列表
                global digital_set_after
                digital_set_after = get_field_to_str(self.field)

                return True
            else:
                return False

    def is_win(self):
        if any(any(i >= self.win_value for i in row) for row in self.field):
            # 更新record表中的信息
            write_file_to_record_update(get_current_battle_id(), self.score, 'Win')
            return True
        else:
            return False

    def is_gameover(self):
        if not any(self.move_is_possible(move) for move in actions1):
            # 更新record表中的信息
            write_file_to_record_update(get_current_battle_id(), self.score, 'Game over')
            return True
        else:
            return False

    def out(self, screen, info):
        screen.addstr(info + '\n')

    def draw(self, screen):
        help_string1 = '(W)Up (S)Down (A)Left (D)Right'
        help_string2 = '     (R)Restart (Q)Exit'
        gameover_string = '           GAME OVER'
        win_string = '          YOU WIN!'
        def cast(string):
            screen.addstr(string + '\n')

        def draw_hor_separator():
            line = '+' + ('+------' * self.width + '+')[1:]
            separator = defaultdict(lambda: line)
            if not hasattr(draw_hor_separator, "counter"):
                draw_hor_separator.counter = 0
            cast(separator[draw_hor_separator.counter])
            draw_hor_separator.counter += 1

        def draw_row(row):
            cast(''.join('|{: ^5} '.format(num) if num > 0 else '|      ' for num in row) + '|')

        screen.clear()
        cast('SCORE: ' + str(self.score)+'      STEP: ' + str(step))
        self.highscore = get_highscore()
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))

        # 获取执行移动前的field列表
        global digital_set_before
        digital_set_before = get_field_to_str(self.field)

        # 画图形，帮助说明文字
        for row in self.field:
            draw_hor_separator()
            draw_row(row)
        draw_hor_separator()
        if self.is_win():
            cast(win_string)
        else:
            if self.is_gameover():
                cast(gameover_string)
            else:
                cast(help_string1)
        cast(help_string2)

    def spawn(self):
        # 随机生成4或者2   2个机率大
        new_element = 4 if randrange(100) > 89 else 2
        # 检测所有的方格中的数字 如果是0 就提交出去
        # choice()方法返回一个列表，元组或字符串的随机一项。 这里面是返回一个没有数字的空的i，j的坐标
        (i, j) = choice([(i, j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element
        coordinate = str(i)+","+str(j)
        battle_id=get_current_battle_id()
        # 插入一个新的操作
        write_file_to_operation_insert(battle_id, step, new_element, coordinate)

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i):  # true if there'll be change in i-th tile
                if row[i] == 0 and row[i + 1] != 0: # Move
                    return True
                if row[i] != 0 and row[i + 1] == row[i]: # Merge
                    return True
                return False
            return any(change(i) for i in range(len(row) - 1))

        check = {}
        check['Left']  = lambda field:                              \
                any(row_is_left_movable(row) for row in field)

        check['Right'] = lambda field:                              \
                 check['Left'](invert(field))

        check['Up']    = lambda field:                              \
                check['Left'](transpose(field))

        check['Down']  = lambda field:                              \
                check['Right'](transpose(field))

        if direction in check:
            return check[direction](self.field)
        else:
            return False

def main(stdscr):

    def init():
        #重置游戏棋盘
        game_field.reset()
        return 'Game'

    def not_game(state):
        #画出 GameOver 或者 Win 的界面
        game_field.draw(stdscr)
        #读取用户输入得到action，判断是重启游戏还是结束游戏
        action = get_user_action(stdscr)
        responses = defaultdict(lambda: state) #默认是当前状态，没有行为就会一直在当前界面循环
        responses['Restart'], responses['Exit'] = 'Init', 'Exit' #对应不同的行为转换到不同的状态
        return responses[action]

    def game():
        time.sleep(0.1)
        # 画出当前棋盘状态
        game_field.draw(stdscr)
        # 读取用户输入得到action
        action = get_machine_direction(game_field.field)
        direction = action
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):  # move successful
            # 操作方向显示到screen上面去
            game_field.out(stdscr, direction)

            # 操作方向和更新前后的field写入数据库
            battle_id=get_current_battle_id()
            global step
            global digital_set_before
            global digital_set_after
            write_file_to_operation_update(battle_id, step, direction, digital_set_before, digital_set_after)
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'

            step += 1

        return 'Game'     # 始终循环Game 方格的移动胜利或者失败或者退出都在Game里面


    state_actions = {
            'Init': init,
            'Win': lambda: not_game('Win'),
            'Gameover': lambda: not_game('Gameover'),
            'Game': game
        }

    curses.use_default_colors()

    # 设置终结状态最大数值为 32
    game_field = GameField(win=2048)

    state = 'Init'

    #状态机开始循环
    while state != 'Exit':
        state = state_actions[state]()
    f.close()
    conn.close()


curses.wrapper(main)