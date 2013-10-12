# -- coding:gbk --
import sys, time, os, re
import urllib, urllib2, cookielib

def get_str_from_text(re_str, text):
	a = re.search(re_str, text)
	if a:
		return a.group(1)
	return ""


loginurl = 'https://www.douban.com/accounts/login'
cookie = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

params = {
"form_email":"terrygon@163.com",
"form_password":"123456test",
"source":"index_nav" #没有的话登录不成功
}

#从首页提交登录
response=opener.open(loginurl, urllib.urlencode(params))

#验证成功跳转至登录页
if response.geturl() == "https://www.douban.com/accounts/login":
	html=response.read()

	#验证码图片地址
	imgurl=re.search('<img id="captcha_image" src="(.+?)" alt="captcha" class="captcha_image"/>', html)
	if imgurl:
		url=imgurl.group(1)
		#将图片保存至同目录下
		res=urllib.urlretrieve(url, 'v.jpg')
		#获取captcha-id参数
		captcha=re.search('<input type="hidden" name="captcha-id" value="(.+?)"/>' ,html)
		if captcha:
			vcode=raw_input('请输入图片上的验证码：')
			params["captcha-solution"] = vcode
			params["captcha-id"] = captcha.group(1)
			params["user_login"] = "登录"
			#提交验证码验证
			response=opener.open(loginurl, urllib.urlencode(params))
			''' 登录成功跳转至首页 '''
			if response.geturl() == "http://www.douban.com/":
				print 'login success ! (have validate image)'
else:
	print 'login success ! (have no validate image)'


#发豆油
doumail_url = "http://www.douban.com/doumail/49589762/"
doumail_url1 = "http://www.douban.com/doumail/write?to=49589762"


for i in range(10):

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
		vcode=raw_input('请输入图片上的验证码：')

	content = u"你好，啦啦啦"

	params = {
	"to":"49589762",
	"action":"m_reply",
	"m_text":content.encode('utf-8'),
	"captcha-id":captcha_id_val, 
	"captcha-solution":vcode,
	"ck":ck_val
	}

	request=urllib2.Request(doumail_url)
	request.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11")
	request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")
	request.add_header("Origin", "http://www.douban.com")
	request.add_header("Referer", "http://www.douban.com/")
	opener.open(request, urllib.urlencode(params))

	print '发送成功'
	time.sleep(30)