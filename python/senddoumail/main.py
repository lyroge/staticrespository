# -- coding:utf-8 --
import sys, time, os, re, datetime, random
import urllib, urllib2, cookielib
from fun import send_doumail, login_douban, random_text_from_keywords
import MySQLdb, MySQLdb.cursors

#接收随机内容豆油的账号地址
doumain_userid = 49589762
doumail_url = "http://www.douban.com/doumail/%d/" % doumain_userid
doumail_url1 = "http://www.douban.com/doumail/write?to=%d" % doumain_userid

#取数据库中用户信息
conn = MySQLdb.connect(host='localhost',user='root',passwd='abc',db='fadouyou',cursorclass=MySQLdb.cursors.DictCursor)
cursor=conn.cursor()
items=[]
cursor.execute("SELECT id, url FROM douyou_user  where content_id is null")
result = cursor.fetchall()
for r in result:
	items.append((r["id"], r["url"]))

#取数据库豆油内容
content = None
cursor.execute("SELECT content_id, content FROM douyou_content")
result = cursor.fetchone()
douyou_content = (result["content_id"], result["content"])

if __name__ == "__main__":

	#login 豆瓣
	login_douban()

	for item in items:
		# 发一次随机内容
		content = random_text_from_keywords().encode('utf-8')
		send_doumail(doumail_url, doumail_url1, doumain_userid, content)

		
		url = item[1]		
		uid = str(url[url.find("to=")+3:])
		
		#发给用户真实豆油
		send_doumail("http://www.douban.com/doumail/%s/" % uid, "http://www.douban.com/doumail/write?to=%s" % uid, uid, douyou_content[1].decode('gb2312').encode('utf-8'))
		sql = "update douyou_user set content_id="+str(douyou_content[0]) + " where id = " + str(item[0])
		cursor.execute(sql)
		conn.commit()

		#time.sleep(1)

cursor.close() 
conn.close()