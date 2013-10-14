# -- coding:utf-8 --
import sys, time, os, re, datetime, random
import urllib, urllib2, cookielib
from fun import send_doumail, login_douban, random_text_from_keywords
import MySQLdb, MySQLdb.cursors

#doumain fist
doumail_url = "http://www.douban.com/doumail/49589762/"
doumail_url1 = "http://www.douban.com/doumail/write?to=49589762"

#doumain second
doumail_url2= "http://www.douban.com/doumail/23416934/"
doumail_url3 = "http://www.douban.com/doumail/write?to=23416934"

send_content = '''
用户 有个标  http://www.douban.com/event/1994032246/
'''

conn = MySQLdb.connect(host='localhost',user='root',passwd='abc',db='fadouyou',cursorclass=MySQLdb.cursors.DictCursor)
cursor=conn.cursor()
items=[]
cursor.execute("SELECT id, url FROM douyou_user  where content_id is null")
result = cursor.fetchall()
for r in result:
	items.append((r["id"], r["url"]))

content = None
cursor.execute("SELECT content_id, content FROM douyou_content")
result = cursor.fetchone()
douyou_content = (result["content_id"], result["content"])

if __name__ == "__main__":

	#login
	login_douban()

	for item in items:
		content = random_text_from_keywords().encode('utf-8')
		send_doumail(doumail_url, doumail_url1, "49589762", content)

		url = item[1]		
		uid = str(url[url.find("to=")+3:])

		send_doumail("http://www.douban.com/doumail/"+uid + "/", "http://www.douban.com/doumail/write?to="+uid, uid, douyou_content[1].decode('gb2312').encode('utf-8'))
		sql = "update douyou_user set content_id="+str(douyou_content[0]) + " where id = " + str(item[0])
		cursor.execute(sql)
		conn.commit()

		#time.sleep(1)

cursor.close() 
conn.close()