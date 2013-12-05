#!/usr/bin/env python
# -*- coding: UTF-8 -*-

url = 'https://www.google.com.hk/search?safe=strict&site=&source=hp&q=leg+warmers'
url = 'http://pgl.yoyo.org/http/browser-headers.php'



from scrapyrobot import ProxyScrapy

curl = ProxyScrapy()

a=curl.get_html_body(url)
print a