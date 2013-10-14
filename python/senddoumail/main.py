# -- coding:utf-8 --
import sys, time, os, re, datetime, random
import urllib, urllib2, cookielib
from fun import send_doumail, login_douban, random_text_from_keywords


#doumain fist
doumail_url = "http://www.douban.com/doumail/49589762/"
doumail_url1 = "http://www.douban.com/doumail/write?to=49589762"

#doumain second
doumail_url2= "http://www.douban.com/doumail/23416934/"
doumail_url3 = "http://www.douban.com/doumail/write?to=23416934"


if __name__ == "__main__":


	#login
	login_douban()

	while True:
		content = random_text_from_keywords().encode('utf-8')
		send_doumail(doumail_url, doumail_url1, "49589762", content)

		for i in range(0,2):
			send_doumail(doumail_url, doumail_url, "23416934", "有个聚会的活动，你知道吗")