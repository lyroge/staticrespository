#!/usr/bin/env python
# -*- coding: UTF-8 -*-

url = 'https://www.google.com.hk/search?safe=strict&site=&source=hp&q=leg+warmers'
url = 'http://pgl.yoyo.org/http/browser-headers.php'


import urllib, urllib2, cookielib, random
from proxy import ProxyRobot
from settings import USER_AGENT_LIST,PROXY_ENABLE

class ProxyScrapy(object):
    def __init__(self):
        self.proxy_robot = ProxyRobot()
        self.current_proxy = None
        self.cookie = cookielib.CookieJar()
    
    def __builder_proxy_cookie_opener(self):        
        cookie_handler = urllib2.HTTPCookieProcessor(self.cookie)        
        handlers = [cookie_handler]

        if PROXY_ENABLE:
            self.current_proxy = ip_port = self.proxy_robot.get_random_proxy()
            proxy_handler = urllib2.ProxyHandler({'http': ip_port[7:]})
            handlers.append(proxy_handler)
        
        opener = urllib2.build_opener(*handlers)
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
        request.add_header("Accept-Encoding", "gzip,deflate,sdch")
        request.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        request.add_header("Cache-Control", "no-cache")
        request.add_header("Connection", "keep-alive")

        try:
            response = opener.open(request)

            http_code = response.getcode()
            if http_code == 200:
                if PROXY_ENABLE:
                    self.proxy_robot.handle_success_proxy(self.current_proxy)
                html = response.read()
                return html
            else:
                if PROXY_ENABLE:
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