mysqldump -u用户名 -p密码 数据库名 表名 --where="筛选条件" > 导出文件路径

0.备份数据库 （表结构、数据都导出）
mysqldump -uroot -pabc freeb2b > fb.bak		√

1.导出结构不导出数据
mysqldump -d 数据库名 -uroot -p > xxx.sql	√

2.导出数据不导出结构
mysqldump -t 数据库名 -uroot -p > xxx.sql

3.导出特定表的结构 --table 参数可以指定多个表
mysqldump -uroot -pabc -B freeb2b --table company product > fb		√

导出某个表中的一些数据
mysqldump -uroot -pabc freeb2b product --where="id=1" > 1.sql		√


***************************************mysqldump支持下列选项：**************************
--add-drop-table   
在每个create语句之前增加一个drop table。   

--allow-keywords   
允许创建是关键词的列名字。这由表名前缀于每个列名做到。   

-c, --complete-insert   
使用完整的insert语句(用列名字)。   


***************************************导入数据：**************************
mysql 数据库名 < 文件名