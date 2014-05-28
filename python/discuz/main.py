# -- coding:utf-8 --

import MySQLdb, MySQLdb.cursors
from const.db import HOST,USER,PASSWD,DB
import random, time, datetime

conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
conn.set_character_set('utf8')
cursor=conn.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

def timestamp(dtstr):
	if not dtstr:
		a = datetime.datetime.now()
	else:
		a=datetime.datetime.strptime(dtstr, '%Y-%m-%d %H:%M')
	t=time.mktime(a.timetuple())
	return t

def post(subject, content, fid, authorid, author, posttime):

	#插入主题
	unixtime = timestamp(posttime)	
	param = (fid, author, authorid, subject, unixtime, unixtime, author)
	cursor.execute('INSERT INTO pre_forum_thread(fid, author, authorid, subject, dateline, lastpost, lastposter) values(%s, %s, %s, %s, %s, %s, %s)', param)
	tid = cursor.lastrowid

	#获取pid pre_forum_post_tableid
	cursor.execute('INSERT INTO pre_forum_post_tableid(pid) values(%s)', ('0',))
	pid = cursor.lastrowid

	#插入主题内容 pre_forum_post
	param = (pid, fid, tid, author, authorid, subject, unixtime, content, '127.0.0.1', '22622')
	cursor.execute('INSERT INTO pre_forum_post (pid, fid, tid, author, authorid, subject, dateline, message, useip, port) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', param)

	#更新论坛版块内容 pre_forum_forum
	lastpost = '%s	%s	%s	%s' % (tid, subject, unixtime, author)
	cursor.execute('update pre_forum_forum set posts=posts+1, todayposts=todayposts+1, lastpost=%s where fid=%s', (lastpost,fid))

	#更新用户统计数据 pre_common_member_count
	cursor.execute('update pre_common_member_count set posts=posts+1, threads=threads+1 where uid=%s', (authorid,))
	print 'done'

post("测试帖子", "测试帖子内容", 69, 12, "资讯小编", "")

cursor.close() 
conn.close()