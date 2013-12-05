#!/usr/bin/env python
# -*- coding: UTF-8 -*-

url = 'https://www.google.com.hk/search?safe=strict&site=&source=hp&q=leg+warmers'
url = 'http://pgl.yoyo.org/http/browser-headers.php'


import urllib, urllib2, cookielib, random
from proxy import ProxyRobot
from settings import USER_AGENT_LIST

class ProxyScrapy(object):
    def __init__(self):
        self.proxy_robot = ProxyRobot()
        self.current_proxy = None
    
    def __builder_proxy_cookie_opener(self):
        self.current_proxy = ip_port = self.proxy_robot.get_random_proxy()
        cookie = cookielib.CookieJar()
        cookie_handler = urllib2.HTTPCookieProcessor(cookie)
        proxy_handler = urllib2.ProxyHandler({'http': ip_port[7:]})

        opener = urllib2.build_opener(proxy_handler, cookie_handler)
        urllib2.install_opener(opener)
        return opener

        '''
        try:
            r=urllib2.urlopen('http://hellocompanies.com', timeout=5)
        except Exception as inst:
            print inst
            return None
        '''
    
    def get_html_body(self,url):
        opener = self.__builder_proxy_cookie_opener()

        request=urllib2.Request(url)
        request.add_header("User-Agent",random.choice(USER_AGENT_LIST))
        request.add_header("Accept-Charset", "GBK,utf-8;q=0.7,*;q=0.3")

        try:
            response = opener.open(request)

            http_code = response.getcode()
            if http_code == 200:
                self.proxy_robot.handle_success_proxy(self.current_proxy)
                html = response.read()
                return html
            else:
                self.proxy_robot.handle_double_proxy(self.current_proxy)
                return self.get_html_body(url)
        except Exception as inst:
            print inst
            self.proxy_robot.handle_double_proxy(self.current_proxy)
            return self.get_html_body(url)

        '''
        for c in cookie:
            print c
        '''