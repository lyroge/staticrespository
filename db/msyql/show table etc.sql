
--show index and engine 索引、引擎信息
	show create table product;

--show size infomation 表的大小信息
	show table status like 'product'\G

--clues of inefficiencies 低效查询线索
	EXPLAIN SELECT * from product limit 1;

-- 展示mysql缓存信息
SHOW VARIABLES LIKE '%buffer%';