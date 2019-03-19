```
2048游戏

这个游戏可以人机对战   ok
也可以机器对战机器
根据现有的游戏攻略，让机器自己选择最佳策略，然后机器操作。
通过迭代游戏攻略策略，逐渐让机器的得分变高。
游戏里面加入sqlite3文件数据库，将得分保存并在下次游戏的时候显示。
数据库也可以用来统计机器对战的成绩，观察迭代后的游戏策略是不是更加优化。

先分析现有的人机对战代码   ok
制作对战策略算法，实现简单的机器对战机器功能。
对战策略迭代，优化对战策略算法，提高机器得分。

通过随机方向，机器对战已经可以使用了，但是完全没有策略可言。
最高分数也就是在3252分。

加入新功能
对战策略生产
数据放入数据库保存 使用sqlite3 文件数据库
放入数据库字段 
对战记录表 record
对战盘的ID	策略版本		对战时间       		分数		失败或者胜利
battle_id	ver float	batle_time  datatime	score  int	result   string
每盘步数记录表 operation
对战盘的ID	当次步数		新增加数字值为（2或者4） 	新增加数字的位置 	
battle_id  int	sept  int       new_digital   int     	coordinate  char	

当次执行的方向       	执行前的各点的数字（一个2维数组）	执行后的各点的数字（一个2维数组）	
Direction  string	digital_set_before  list	digital_set_after  list

```
