'''
2013/3/7
set proxy from http://51dai.li
'''

from scrapy.exceptions import IgnoreRequest,CloseSpider
from scrapy.http import Request,Response,TextResponse,HtmlResponse 
from scrapy.selector import HtmlXPathSelector
import random, urllib2, os
from settings import PROXY_TEST_URL,PROXY_URL,PROXY_URL_DICT,PROXY_TEST_TIMEOUT,SKIP_PROXY_TEST

class ProxyRobot(object): 
    def __init__(self):
        self.PROXY_FILE = 'proxy/proxies.txt'
        self.proxy_test_url = PROXY_TEST_URL
        self.proxies = []
        self.PROXY_ERROR_COUNT = {}
        self._get_proxy_from_file()
        if not self.proxies:
            self._get_proxy_from_website()

        self.i = 0
        self.j=random.randint(1, 1)
        self.proxy = random.choice(self.proxies) if self.proxies else None

    def get_random_proxy(self):
        if  self.i == self.j:
            self.i = 0
            self.j = random.randint(1, 1)

            #get proxy list from website again
            if (not self.proxies) or len(self.proxies) == 0:
                self._get_proxy_from_website()

            if self.proxies:
                self.proxy = random.choice(self.proxies)
        self.i = self.i + 1
        return self.proxy

    def handle_double_proxy(self, current_proxy):
        if current_proxy in self.PROXY_ERROR_COUNT:
            self.PROXY_ERROR_COUNT[current_proxy] = self.PROXY_ERROR_COUNT[current_proxy] + 1

            #remove 
            if self.PROXY_ERROR_COUNT[current_proxy] >= 10:
                del self.PROXY_ERROR_COUNT[current_proxy]
                self.proxies.remove(current_proxy)
                print '\r\n remove proxy : %s' % current_proxy

                #update proxy list file
                if self.proxies:
                    self._update_proxy_list_to_file()
        else:
            self.PROXY_ERROR_COUNT[current_proxy] = 1
        
        #renew proxy 
        self.i = self.j = 0
        return None

    def handle_success_proxy(self, current_proxy):
        if current_proxy in self.PROXY_ERROR_COUNT:
            del self.PROXY_ERROR_COUNT[current_proxy]

    def _get_proxy_from_file(self):
        if os.path.exists(self.PROXY_FILE):
            with open(self.PROXY_FILE) as f:
                for line in f.readlines():
                    http_ip_port = line.strip(os.linesep)
                    if not http_ip_port:
                        continue
                    if not SKIP_PROXY_TEST:
                        isok = self._test_proxy_ok_or_not(http_ip_port[7:])
                        if isok:
                            self.proxies.append(http_ip_port)
                    else:
                        self.proxies.append(http_ip_port)
                return self.proxies
        return None

    def _get_proxy_from_website(self):
        if not os.path.exists('proxy'):
            os.mkdir('proxy') 
        with open(self.PROXY_FILE, 'w+') as f:
            response = urllib2.urlopen(PROXY_URL_DICT[PROXY_URL]) 
            scrapy_reponse = HtmlResponse(url=response.url, body=response.read())
            hxs = HtmlXPathSelector(scrapy_reponse)
            trs = hxs.select('//*[@id="tb"]/table/tr')
            for tr in trs:
                ip = ''.join(tr.select('td[2]/text()').extract())
                port = ''.join(tr.select('td[3]/text()').extract())
                regions = ''.join(tr.select('td[4]/text()').extract())
                if ip and port and regions == 'CN':
                    ip_port = '%s:%s' % (ip, port)

                    isok = self._test_proxy_ok_or_not(ip_port)
                    if isok:
                        http_ip_port = 'http://' + ip_port
                        self.proxies.append(http_ip_port)
                        if f:
                            f.write(http_ip_port + os.linesep)
                            f.flush()


    def _test_proxy_ok_or_not(self, ip_port):
        proxy = urllib2.ProxyHandler({'http': ip_port})
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        try:
            r=urllib2.urlopen(self.proxy_test_url, timeout=PROXY_TEST_TIMEOUT)
            if r:
                print ip_port + ' is ok!'
                return True
        except Exception as inst:
            print inst
        return False

    def _update_proxy_list_to_file(self):
        with open(self.PROXY_FILE, 'w+') as f:
            for proxy in self.proxies:
                f.write(proxy + os.linesep)