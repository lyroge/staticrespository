# -- coding:utf-8 --
import sys, time, os, re, datetime, random
import urllib, urllib2, cookielib
from fun import send_doumail, login_douban


#doumain fist
doumail_url = "http://www.douban.com/doumail/49589762/"
doumail_url1 = "http://www.douban.com/doumail/write?to=49589762"

#doumain second
doumail_url2= "http://www.douban.com/doumail/23416934/"
doumail_url3 = "http://www.douban.com/doumail/write?to=23416934"


if __name__ == "__main__":

	#login
	login_douban()

	for i in range(1,61):
		if (i == 1 or i % 2 == 0):
			content = random.choice(["今天是你的生日，恭喜生日快乐", "It doesn't matter how many times you fail.", "It's point that how many times you stand ", "失败多少次不重要,只要站起来比倒下去的次数多一次就是成功！","周一，加油啊！ 亲", "按照这样的计算法则， 我们无法成为朋友", "hi, 美女， 约会吗 ？？ ", "every Tom 的意思是?", "如何用英语自然表达“爱你”？", "这里是你的主页，用来展示你的生活和发现", "http://www.douban.com/doumail 豆油我吧", "恩  时间还可以的", "不是不行吗 ？ 你一看我就是人工发啊", ""])
			send_doumail(doumail_url, doumail_url1, "49589762", content)
		else:
			send_doumail(doumail_url2, doumail_url3, "23416934", "有个聚会的活动，你知道吗")

		time.sleep(random.randint(5,10))