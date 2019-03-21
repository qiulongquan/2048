```
2048游戏

注意
先默认生成2个数字，前2次是不能操作的。
2个随机位置生成数字完成后，第三次开始可以操作方向。
顺序是：
先移动（移动是整体移动到头，不是移动一步）
后合并（合并是内侧开始向外侧合并，合并一次）
最后随机位置显示新的数字

2048 AI
通过算法实现AI自动寻找解决方案　　重点
https://github.com/ovolve/2048-AI
2048 AI 程序算法分析
http://blog.jobbole.com/64597/
2048游戏的最佳算法是？来看看AI版作者的回答
http://blog.jobbole.com/63888/


这个游戏可以人机对战   ok
也可以机器对战机器
根据现有的游戏攻略，让机器自己选择最佳策略，然后机器操作。
通过迭代游戏攻略策略，逐渐让机器的得分变高。
游戏里面加入sqlite3文件数据库，将得分保存并在下次游戏的时候显示。   Ok
数据库也可以用来统计机器对战的成绩，观察迭代后的游戏策略是不是更加优化。

先分析现有的人机对战代码   ok
制作对战策略算法，实现简单的机器对战机器功能。
对战策略迭代，优化对战策略算法，提高机器得分。

通过随机方向，机器对战已经可以使用了，但是完全没有策略可言。
最高分数也就是在3252分。

加入新功能
对战策略生产
数据放入数据库保存 使用sqlite3 文件数据库   ok
放入数据库字段   ok
对战记录表 record
对战盘的ID	策略版本		对战时间       		分数		  胜利分数条件		宽度			高度			失败或者胜利
battle_id  int	ver string	battle_time  TimeStamp	score  int	  win_score  int	width  string		height  string	result   string


每盘步数记录表 operation
对战盘的ID	当次步数		新增加数字值为（2或者4） 	新增加数字的位置 	
battle_id  int	step  int       new_digital   int     	coordinate  char	

当次执行的方向       	执行前的各点的数字（一个2维数组）	执行后的各点的数字（一个2维数组）	
Direction  string	digital_set_before  list	digital_set_after  list



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


```
