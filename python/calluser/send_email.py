#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

def send_email(to, title, *holdplace):
	username = 'freeb2bmarket@gmail.com'
	password = 'fbm61902279'

	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = title
	msgRoot['From'] = username
	msgRoot['To'] = to
	msgRoot.preamble = 'This is a multi-part message in MIME format.'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	f=open('email.txt', 'r')
	msg = f.read()
	f.close()
	msg = msg % holdplace
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

	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)

	server.sendmail(username, to, msgRoot.as_string())
	server.quit()