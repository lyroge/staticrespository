import MySQLdb, MySQLdb.cursors
from send_email import send_email
from const.db import HOST,USER,PASSWD,DB,START_URL_SQL
import random, time

conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
cursor=conn.cursor()
requests=[]
cursor.execute(START_URL_SQL)
result = cursor.fetchall()
for r in result:
	url = '<a href="http://www.freeb2bmarket.com/company/%s.html">%s</a>' % (r['url_slug'], r['name'])
	person = r['contactperpon']
	email = r['email']
	title = '%s Product details required' % person
	send_email(email, title, person, url)
	print r['name']
	time.sleep(random.choice([1,3,5,7]))
cursor.close() 
conn.close()