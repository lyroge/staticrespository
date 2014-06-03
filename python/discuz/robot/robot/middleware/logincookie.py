from scrapy.exceptions import IgnoreRequest,CloseSpider
from scrapy.http import Request,Response,TextResponse,HtmlResponse 
from scrapy.selector import HtmlXPathSelector
import random, urllib2, os, re, time, socket, requests


class LoginCookieMiddleware(object): 
    def process_request(self, request, spider):
        if  '/job/zhaopin.asp' in request.url:
            request.cookies['Hm_lpvt_f1961cf0e79eb47b6453fde97abcf86e'] = '1401696290'
            request.cookies['Hm_lvt_f1961cf0e79eb47b6453fde97abcf86e'] = '1401583459,1401693745,1401696003,1401696268'
            request.cookies['pgv_pvi'] = '761379326'
            request.cookies['AJSTAT_ok_times'] = '1'
            request.cookies['ASPSESSIONIDQSTDBTDR'] = 'OGDKJGIBGJJIAHAEPACCMIDH'
            request.cookies['bdshare_firstime'] = '1392548114409'
            request.cookies['echang%2Ecn'] = 'hypwd=d41d8cd98f00b204e9800998ecf8427e&huiyuan=%D0%A1%5F%B8%D5'