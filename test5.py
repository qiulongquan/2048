# -*- coding: utf-8 -*-
# sqlite3 schema
import sqlite3
from contextlib import closing

dbname = 'operation.sqlite3'

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()

    # executeメソッドでSQL文を実行する
    create_table = '''create table IF NOT EXISTS record (
                        battle_id INTEGER PRIMARY KEY,
                        ver CHAR(20),
                        battle_time TimeStamp NOT NULL DEFAULT (datetime('now','localtime')),
                        score INTEGER,
                        win_score INTEGER,
                        width CHAR(20),
                        height CHAR(20),
                        result CHAR(50)
                        )'''
    c.execute(create_table)

    create_table = '''create table IF NOT EXISTS operation (
                        battle_id INTEGER, 
                        step INTEGER,
                        new_digital INTEGER, 
                        coordinate CHAR(20),
                        Direction CHAR(20),
                        digital_set_before CHAR(2000),
                        digital_set_after CHAR(2000)
                        )'''
    c.execute(create_table)


    # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
    # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
    # タプルで渡す．

    # sql = 'insert into record ( battle_id, ver, score,result) values (?,?,?,?)'
    # record = (4, '1.0', 20, 'success')
    # c.execute(sql, record)

    sql = 'insert into operation (' \
              'battle_id,' \
              'step,' \
              'new_digital,' \
              'coordinate,' \
              'Direction,'\
              'digital_set_before,'\
              'digital_set_after'\
              ') values (?,?,?,?,?,?,?)'
    record = (1, 0, 2, '0,0', '','','')
    c.execute(sql, record)

    # # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
    # # executemanyメソッドを実行する
    # insert_sql = 'insert into users1 (id, name, age, gender) values (?,?,?,?)'
    # users1 = [
    #     (2, 'Shota', 54, 'male'),
    #     (3, 'Nana', 40, 'female'),
    #     (4, 'Tooru', 78, 'male'),
    #     (5, 'Saki', 31, 'female')
    # ]
    # c.executemany(insert_sql, users1)
    conn.commit()

    select_sql = 'select * from record'
    for row in c.execute(select_sql):
        print(row)
    select_sql = 'select * from operation'
    for row in c.execute(select_sql):
        print(row)
    conn.close()