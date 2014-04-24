# -- coding:utf-8 --

from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,HtmlResponse
import re, os, random, codecs, requests


f=codecs.open('1.txt', 'w', encoding="utf-8")

ary = []
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36'}
for i in range(1, 21):
    url = "http://www.aibang.com/?area=bizsearch2&cmd=bigmap&city=%E5%8C%97%E4%BA%AC&ufcate=%E7%BE%8E%E9%A3%9F&a=%E5%B9%B3%E8%B0%B7%E5%9F%8E%E5%8C%BA&q=&rc=1&as=5000&apr=0%7C0&quan=1&p=" + str(i)

    response = requests.get(url, headers=headers)
    body = response.text
    response = HtmlResponse(url='', body=body, encoding=response.encoding)
    hxs = HtmlXPathSelector(response)

    items = hxs.select('//*[@class="bizshow"]//div[@bi]')
    for item in items:
        img = ''.join(item.select('div[@class="imgvc"]//img/@src').extract())
        b = ''.join(item.select('div[@class="imgvc"]//a/@href').extract())

        t = ''.join(item.select('div[@class="aside"]/h4/a/text()').extract())
        a = '\r\n'.join(item.select('div[@class="aside"]/div[@class="part1"]/p[position()<last()]/descendant-or-self::text()').extract())
        
        #self.cursor.execute("INSERT INTO empirecms.weixin_data (Title, Description, CreateTime, xh) VALUES (%s, %s, now(), 5)", (t, a))
        ary.append("%s\r\n%s" % (t, a))

#ary.reverse()
f.write('\r\n\r\n'.join(ary))


