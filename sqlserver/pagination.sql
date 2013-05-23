
//sql2005  row_number 分页方法
select * from (select row_number() over(order by id desc) as rownum, * from testtable) a where rownum between 11 and 20 --闭区间

//not top分页方法 （不在前多少页）
select top 10 * from testtable where id not in (select top 10 id from testtable order by id desc ) order by id desc 

//取top记录最大（小的记录），然后再取id大（小）的top记录
select top 10 * from testtable where id < (select min(id) from (select top 10 id from testtable order by id desc) a) order by id desc 


总结：（2,3道理类似）
1. sqlserver 2005  row_number() over 分页
2. 不在top列表
3. 取top列表边界id值进行比较


