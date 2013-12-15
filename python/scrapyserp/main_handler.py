#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re,pytz,os,thread,time,threading
tz=pytz.timezone('Asia/Chongqing')

from collections import OrderedDict
from datetime import datetime
from scrapyrobot import ProxyScrapy
from pyquery import PyQuery as pq
from time import clock
import MySQLdb.cursors
curl = ProxyScrapy()
from const.db import HOST,USER,PASSWD,DB

import tornado.ioloop
import tornado.web
from tornado import template
import urllib 

mylock = thread.allocate_lock()

class ResultThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)  
        self.func = func
        self.args = args  
   
    def run(self):
        self.func(*self.args)


URL_TEMPLATE = 'http://www.alibaba.com/products/F0/%s/%s.html'

def search_keywords_rank(keyword_company_name, keywords):
    def get_context(url):
        html=curl.get_html_body(url)
        d = pq(html)
        items = d("#J-items-content .ls-item")
        items_c = len(items)
        print "[%d items] - %s" % (items_c, url)
        return items, items_c

    def get_result(result, u, page_index):
        items, items_c = get_context(u)
        b = False
        for item_index in range(0, items_c):
            e=items.eq(item_index).find('.title a')
            p_title = e.text()
            p_url = e.attr('href')

            e=items.eq(item_index).find('.cright h3 .dot-product')
            company_name = e.text()
            company_url = e.attr('href')

            if  keyword_company_name in company_url:
                total_index = (page_index-1)*38 +item_index+1+(0 if page_index==1 else 5)
                print 'page %s, index %s, total index %s' % (page_index, item_index+1, total_index)
                b = True

                if keyword not in result:
                    mylock.acquire()
                    result[keyword] = (p_title, p_url, page_index, item_index+1, total_index, u)
                    mylock.release()
                else:
                    mylock.acquire()
                    if result[keyword][2] > page_index or (result[keyword][2] == page_index and result[keyword][3] > item_index+1):
                        result[keyword] = (p_title, p_url, page_index, item_index+1, total_index, u)
                    mylock.release()
                break

    result = OrderedDict()
    for keyword in keywords:
        threads = []
        for page_index in range(1,9):
            u = URL_TEMPLATE % (re.sub('\s+', '_', keyword.strip()), page_index)
            t = ResultThread(get_result, (result, u, page_index))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
    return result


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html', books={}, companyname='', keywords='')

    def post(self):
        company_name=self.get_argument('companyname').strip()
        kw=keywords = self.get_argument('keywords').strip()

        result = {}
        if not company_name or not keywords:
            self.write('company name or keywords can\'t empty')
        else:
            keywords = re.split('\r\n|,', keywords)
            keywords = [kw for kw in keywords if kw]
            result=search_keywords_rank(company_name, keywords[:5]) #single execute

            conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
            conn.set_character_set('utf8')
            cursor=conn.cursor()
            cursor.execute('SET NAMES utf8;')
            cursor.execute('SET CHARACTER SET utf8;')
            cursor.execute('SET character_set_connection=utf8;')

            keys = result.keys()
            values = [company_name for v in keys]
            cursor.executemany('insert into ali_keyword(name,companyurl) values(%s,%s)', zip(keys,values))
            cursor.close() 
            conn.close()
        self.render('index.html', books=result, companyname=company_name, keywords=kw)

application = tornado.web.Application([
    (r"/keywordtool/", MainHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()