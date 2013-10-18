#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

def send_email(to, title):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = title
	msgRoot['From'] = 'freeb2bmarket@gmail.com'
	msgRoot['To'] = to
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	f=open('email.txt', 'r')
	msg = f.read()
	f.close()
	msgText = MIMEText(msg, 'html')
	msgAlternative.attach(msgText)

	'''
	msg = "\r\n".join([
	  "From: %s" % fromaddr,
	  "To: %s" % toaddrs,
	  "Subject: Just a message",
	  "",
	  msg
	  ])
	'''

	username = 'freeb2bmarket@gmail.com'
	password = '***'

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)

	server.sendmail(fromaddr, toaddrs, msgRoot.as_string())
	server.quit()