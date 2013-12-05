#!/usr/bin/env python
# -*- coding: UTF-8 -*-

url = 'http://www.google.com.hk/search?q=leg+warmers&safe=strict&hl=zh-HK&gbv=1&ei=rjCgUpfxPMSFiQeJwoHYDQ&start=%s&sa=N'
#url = 'http://pgl.yoyo.org/http/browser-headers.php'



from scrapyrobot import ProxyScrapy

curl = ProxyScrapy()

for i in [0, 10, 20]:
	a=curl.get_html_body(url % str(i))
	f=open('%s.txt' % str(i), 'w')
	f.write(a)