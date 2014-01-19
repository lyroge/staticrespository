#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import MySQLdb, MySQLdb.cursors
from const.db import HOST,USER,PASSWD,DB,START_URL_SQL,EMAIL_USERNAME,EMAIL_PASSWORD

f=open('email.txt', 'r')
msg = f.read()
f.close()


def send_email(to, title, content):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = title
	msgRoot['From'] = 'freeb2bmarket@gmail.com'
	msgRoot['To'] = to
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText(msg.replace('{{content}}', content), 'html')
	msgAlternative.attach(msgText)

	username = EMAIL_USERNAME
	password = EMAIL_PASSWORD

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(EMAIL_USERNAME,EMAIL_PASSWORD)

	server.sendmail(msgRoot['From'], to, msgRoot.as_string())
	server.quit()


conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
cursor=conn.cursor()
requests=[]
cursor.execute(START_URL_SQL)
result = cursor.fetchall()
for r in result:
	id = r['id']
	title = r['subject']
	content = r['message']
	email = r['email']
	print email
	send_email(email, title, content)
	cursor.execute('update inquires set issend=1 where id=%s', (id,))
cursor.close() 
conn.close()