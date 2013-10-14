# -- coding:utf-8 --
import sys, time, os, re, datetime, random
import urllib, urllib2, cookielib

login_url = 'https://www.douban.com/accounts/login'
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

def get_str_from_text(re_str, text):
	a = re.search(re_str, text)
	if a:
		return a.group(1)
	return ""

def login_douban():
	params = {
	"form_email":"terrygon@163.com",
	"form_password":"123456test",
	"source":"index_nav"
	}
	response=opener.open(login_url, urllib.urlencode(params))
	if response.geturl() == "https://www.douban.com/accounts/login":
		html=response.read()
		captcha=get_str_from_text('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html)
		imgurl=get_str_from_text('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
		urllib.urlretrieve(imgurl, 'v.jpg')
		vcode=raw_input('enter validate code:')
		params["captcha-solution"] = vcode
		params["captcha-id"] = captcha
		params["user_login"] = "登录"
		response=opener.open(login_url, urllib.urlencode(params))
		if response.geturl() == "http://www.douban.com/":
			print 'login success !'
	else:
		print 'login success !'

def random_text_from_keywords():
	f=open("keywords.txt", "r")
	text = f.read().decode('utf-8')

	s = u"";
	for i in range(random.randint(7, 15), random.randint(19, 515)):
		s = s + text[random.randint(1, len(text))];
	return s


def send_doumail(doumail_url, doumail_url1, userid, content):
	try:
		response=opener.open(doumail_url)
	except:
		response=opener.open(doumail_url1)
		doumail_url = doumail_url1

	html=response.read()	
	ck_val = get_str_from_text('<input type="hidden" name="ck" value="(.+?)"/>', html)
	captcha_id_val = get_str_from_text('<input type="hidden" name="captcha-id" value="(.+?)"/>', html)
	captcha_img_val = get_str_from_text('<img src="(.+?)" alt="captcha"/>', html)

	vcode=''
	if captcha_id_val:
		#将图片保存至同目录下
		res=urllib.urlretrieve(captcha_img_val, 'v.jpg')
		vcode=raw_input('enter validate code:')

	m_submit = "好了，寄出去"

	params = {
	"to":userid,
	"action":"m_reply",
	"m_text": content ,
	"captcha-id":captcha_id_val, 
	"captcha-solution":vcode,
	"ck":ck_val,
	"m_submit":m_submit
	}

	request=urllib2.Request(doumail_url)
	request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11")
	request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
	request.add_header("Referer", doumail_url)
	opener.open(request, urllib.urlencode(params))

	print 'send success'

