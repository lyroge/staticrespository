#!/usr/bin/env python
# -*- coding: UTF-8 -*-

keyword_company_name = 'Tianjin Wantex Import And Export Co., Ltd.'

url = 'https://www.google.com.hk/search?hl=en&num=10&q=leg+warmers'
url = 'http://www.alibaba.com/products/F0/%s/%s.html'

import re,pytz
tz=pytz.timezone('Asia/Chongqing')

from collections import OrderedDict
from datetime import datetime
from scrapyrobot import ProxyScrapy
from pyquery import PyQuery as pq
from time import clock
import MySQLdb.cursors
curl = ProxyScrapy()
from const.db import HOST,USER,PASSWD,DB

def search_keywords_rank(keyword_company_name, keywords):
    def get_context(url):
        start=clock()
        html=curl.get_html_body(url)
        finish=clock()
        print url,(finish-start)

        d = pq(html)
        items = d("#J-items-content .ls-item")
        items_c = len(items)
        print items_c
        if items_c < 38:
            return get_context(url)
        return items, items_c

    result = OrderedDict()
    for keyword in keywords:
        for page_index in range(1,11):
            u = url % (re.sub('\s+', '_', keyword.strip()), page_index)
            items, items_c = get_context(u)
            b = False
            for item_index in range(0, items_c):
                '''e=items.eq(item_index).find('.title a')
                title = e.text()
                url = e.attr('@href')'''

                e=items.eq(item_index).find('.cright h3 .dot-product')
                company_name = e.text()
                company_url = e.attr('href')

                if  keyword_company_name in company_url:
                    total_index = (page_index-1)*38 +item_index+1+(0 if page_index==1 else 5)
                    print 'page %s, index %s, total index %s' % (page_index, item_index+1, total_index)
                    b = True
                    if keyword not in result:
                        result[keyword] = (page_index, item_index+1, total_index, u)
                    break
            if b:
                break
    return result


if __name__ == '__main__':
        conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
        conn.set_character_set('utf8')
        cursor=conn.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')

        keyword_cache = {}
        cursor.execute("select id,name from ali_keyword")
        rows = cursor.fetchall()
        for row in rows:
            name = row["name"].strip()
            id = row["id"]
            if name not in keyword_cache:
                keyword_cache[name] = id
            a=search_keywords_rank('winbodigital.en.alibaba.com', [name]) #single execute

            for k,v in a.iteritems():
                cur_dt = datetime.now(tz).strftime('%Y-%m-%d')
                cursor.execute("select count(1) as c from ali_keyword_log where kwid=%s and logdate=%s", (keyword_cache[k],cur_dt))
                c=cursor.fetchone()
                if c['c'] > 0:
                    cursor.execute("update ali_keyword_log set lastupdatetime=now(), pageindex=%s,itemindex=%s,totalindex=%s WHERE  kwid=%s and logdate=%s", (v[0],v[1],v[2],keyword_cache[k],cur_dt))
                else:
                    cursor.execute("INSERT INTO ali_keyword_log (kwid, logdate, pageindex, itemindex, totalindex, ali_url, fbr, chuchuang) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (keyword_cache[k],cur_dt,v[0],v[1],v[2],v[3],'',0))