# -*- coding:utf-8 -*-

import curses
import time
import sqlite3
from contextlib import closing
from random import randrange, choice  # generate and place new tile
from collections import defaultdict

letter_codes = [ord(ch) for ch in 'RQrq']
actions = ['Restart', 'Exit']
actions_dict = dict(zip(letter_codes, actions * 2))
actions1 = ['Up', 'Left', 'Down', 'Right']
# 步数 当前是策略的第几步
step=0
# 当前的对战id号
battle_id=0

# 链接sqlite3数据库
dbname = 'operation.sqlite3'
conn = sqlite3.connect(dbname)
c = conn.cursor()


# 操作数据和每个方格的数字信息写入文件
f = open('operation_log.txt', 'a+')


def write_file(height='', width='', win='',field = ''):
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

def write_file_to_operation(battle_id,step=0,action='',field_before='',field_after=''):
    #  4*4的数组里面的数字变换成文字列然后写入文件
    row_str = ''
    row_str_all = ''
    for row in field:
        for i in range(len(row)):
            maped_num = map(str, row)  # 格納される数値を文字列にする
            row_str = ','.join(maped_num)
        row_str_all += " "+row_str

    sql = 'insert into operation (' \
          'battle_id,' \
          'step,' \
          'new_digital,' \
          'coordinate,' \
          'Direction,' \
          'digital_set_before,' \
          'digital_set_after' \
          ') values (?,?,?,?,?,?,?)'
    record = (battle_id,1,2,'','',row_str_all,'')
    c.execute(sql, record)
    conn.commit()

def write_file_to_record(battle_id=0,ver='', batle_time=time.localtime(), score=0,win_score=2048, width='4',height='4',result=''):
    row_str = ''
    row_str_all = ''
    for row in field:
        for i in range(len(row)):
            maped_num = map(str, row)  # 格納される数値を文字列にする
            row_str = ','.join(maped_num)
        row_str_all += " "+row_str

    sql = 'insert into operation (' \
          'battle_id,' \
          'sept,' \
          'new_digital,' \
          'coordinate,' \
          'Direction,' \
          'digital_set_before,' \
          'digital_set_after' \
          ') values (?,?,?,?,?,?,?)'
    record = (1,1,2,'','',row_str_all,'')
    c.execute(sql, record)
    conn.commit()

# 获取得分最多的时候的分数
def get_highscore():
    sql='select max(score) from record;'
    highscore=c.execute(sql)
    if highscore is None or highscore=='':
        highscore=0
    return highscore

def get_battle_id():
    sql = 'select max(battle_id) from record;'
    battle_id = c.execute(sql)
    if battle_id is None or battle_id == '':
        battle_id = 1
    else:
        battle_id += 1
    return battle_id

# 键盘值的获取，如果不在actions_dict里面就继续监听按键，如果在actions_dict里面就返回对应的操作。
def get_user_action(keyboard):
    char = "N"
    while char not in actions_dict:
        char = keyboard.getch()
    return actions_dict[char]


def get_machine_direction():
    direction=choice(actions1)
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
        step=0
        self.field = [[0 for i in range(self.width)] for j in range(self.height)]
        # 获取的初期field的数值写入文件和数据库
        battle_id = get_battle_id()
        write_file(height=str(self.height), width=str(self.width), win='2048',field=self.field)
        write_file_to_record(battle_id,ver='1.0',win_score=2048,width=str(self.width),height=str(self.height))

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
        moves['Left']  = lambda field:                              \
                [move_row_left(row) for row in field]
        moves['Right'] = lambda field:                              \
                invert(moves['Left'](invert(field)))
        moves['Up']    = lambda field:                              \
                transpose(moves['Left'](transpose(field)))
        moves['Down']  = lambda field:                              \
                transpose(moves['Right'](transpose(field)))

        if direction in moves:
            if self.move_is_possible(direction):
                self.field = moves[direction](self.field)
                self.spawn()
                return True
            else:
                return False

    def is_win(self):
        return any(any(i >= self.win_value for i in row) for row in self.field)

    def is_gameover(self):
        return not any(self.move_is_possible(move) for move in actions1)

    def out(self,screen,info):
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
        cast('SCORE: ' + str(self.score))
        if 0 != self.highscore:
            cast('HIGHSCORE: ' + str(self.highscore))

        write_file(field=self.field)
        write_file_to_sqlite3(field=self.field)

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
        (i,j) = choice([(i,j) for i in range(self.width) for j in range(self.height) if self.field[i][j] == 0])
        self.field[i][j] = new_element

    def move_is_possible(self, direction):
        def row_is_left_movable(row):
            def change(i): # true if there'll be change in i-th tile
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
        #画出当前棋盘状态
        game_field.draw(stdscr)
        # out(stdscr)
        #读取用户输入得到action
        action = get_machine_direction()
        # out(stdscr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action): # move successful
            game_field.out(stdscr,action)
            # 操作方向和更新前后的field写入数据库
            global step
            step += 1
            write_file_to_operation(battle_id,step,action, field_before=self.field,field_after=self.field)
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
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