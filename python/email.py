#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import smtplib

fromaddr = 'freeb2bmarket@gmail.com'
toaddrs  = 'lyroge@foxmail.com'
msg = 'Why,Oh why!'

username = 'freeb2bmarket@gmail.com'
password = '***'

server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)

server.sendmail(fromaddr, toaddrs, msg)
server.quit()