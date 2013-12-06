#!/usr/bin/env python
# -*- coding: UTF-8 -*-

keyword_company_name = 'Tianjin Wantex Import And Export Co., Ltd.'

url = 'https://www.google.com.hk/search?hl=en&num=10&q=leg+warmers'
url = 'http://www.alibaba.com/products/F0/%s/%s.html'

import re
from collections import OrderedDict
from scrapyrobot import ProxyScrapy
from pyquery import PyQuery as pq
from time import clock
curl = ProxyScrapy()

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
        for page_index in range(1,21):
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
                    print 'page %d, index %d, total index %d' % (page_index, item_index+1, total_index)
                    b = True
                    if keyword not in result:
                        result[keyword] = (page_index, item_index+1, total_index, u)
                    break
            if b:
                break
    return result


a=search_keywords_rank('winbodigital.en.alibaba.com', ['security products','camera video camera'])
print a