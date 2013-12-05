#!/usr/bin/env python
# -*- coding: UTF-8 -*-

url = 'https://www.google.com.hk/search?hl=en&num=10&q=leg+warmers'
#url = 'http://pgl.yoyo.org/http/browser-headers.php'
url = 'http://www.alibaba.com/products/F0/leg_warmers/%s.html'

from scrapyrobot import ProxyScrapy
from pyquery import PyQuery as pq
from time import clock

keyword_company_name = 'Tianjin Wantex Import And Export Co., Ltd.'

curl = ProxyScrapy()

for page_index in range(1,21):
	u = url % page_index	
	start=clock()
	html=curl.get_html_body(u)
	finish=clock()
	print u,(finish-start)/1000000

	d = pq(html)
	items = d("#J-items-content .ls-item")
	items_c = len(items)

	b = False
	for item_index in range(0, items_c):
		'''e=items.eq(item_index).find('.title a')
		title = e.text()
		url = e.attr('@href')'''

		e=items.eq(item_index).find('.cright h3 .dot-product')
		company_name = e.text()
		company_url = e.attr('href')

		if company_name == keyword_company_name:
			print 'page %d, index %d' % (page_index, item_index+1)
			b = True
			break
	
	if b:
		break


	#f=open('1.html', 'w')
	#f.write(a)