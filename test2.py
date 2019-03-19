# -*- coding: utf-8 -*-
# 生成一个curses的initscr实例 然后显示出来
# 可以输入文字  按键q退出
import curses
import time

def curses_main(args):
    w = curses.initscr()
    curses.echo()
    while 1:
        w.addstr(0, 0, ">")
        w.clrtoeol()
        s = w.getstr()
        str1 = str(s, 'utf-8')    # bytes转字符串方式一
        if str1=='q':break
        w.insertln()
        w.addstr(1, 0, "[" + str(s) + "]")
        f = open('log.txt', 'a+')
        f.write(str(s)+"\n")


curses.wrapper(curses_main)