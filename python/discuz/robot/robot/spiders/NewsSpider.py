# -- coding:utf-8 --

import re, os, random, datetime, time, hashlib, pytz
import MySQLdb, MySQLdb.cursors

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.shell import inspect_response

from robot.const.db import HOST,USER,PASSWD,DB

tz = pytz.timezone('Asia/Shanghai')

#url md5加密
def md5(s):
    return hashlib.md5(s).hexdigest()

#获取时间戳
def timestamp(dtstr):
    if not dtstr:
        a = datetime.datetime.now(tz)
    else:
        a=datetime.datetime.strptime(dtstr, '%Y-%m-%d %H:%M')
    t=time.mktime(a.timetuple())
    return t

class NewsSpider(CrawlSpider):
    name = "News"
    allowed_domains = []

    start_urls = ['http://news.163.com/','http://bj.house.163.com/']

    rules = (
        #163新闻
        Rule(SgmlLinkExtractor(unique=True,allow=('http://news.163.com/\d{1,2}/\d{1,4}/\d{1,2}/\w+.html$'),restrict_xpaths=('//div[@id="news"]/h2/a',)), callback='parse_163_news'),

        #163房产
        Rule(SgmlLinkExtractor(unique=True,allow=('http://bj.house.163.com/\d{1,2}/\d{1,4}/\d{1,2}/\w+.html$'),restrict_xpaths=('//div[@class="mod-list main-list news-date-list on"][position()=1]//a',)), callback='parse_163_house')
    ,)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def __init__(self):
        #打开数据库
        self.conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
        self.conn.set_character_set('utf8')
        self.cursor=self.conn.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')
        #super init 
        super(NewsSpider, self).__init__()

    def post(self, subject, content, fid, authorid, author, posttime, typeid, htmlon=0, bbcodeoff=0):
        #插入主题
        unixtime = timestamp(posttime)  
        param = (fid, author, authorid, subject, unixtime, unixtime, author, typeid, random.randint(8, 51))
        self.cursor.execute('INSERT INTO pre_forum_thread(fid, author, authorid, subject, dateline, lastpost, lastposter, typeid, views) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', param)
        tid = self.cursor.lastrowid

        #获取pid pre_forum_post_tableid
        self.cursor.execute('INSERT INTO pre_forum_post_tableid(pid) values(%s)', ('0',))
        pid = self.cursor.lastrowid

        #插入主题内容 pre_forum_post [htmlon=1, bbcodeoff=-1] 允许帖子中html代码
        param = (pid, fid, tid, author, authorid, subject, unixtime, content, '127.0.0.1', '22622', htmlon, bbcodeoff)
        self.cursor.execute('INSERT INTO pre_forum_post (pid, fid, tid, author, authorid, subject, dateline, message, useip, port, htmlon, bbcodeoff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', param)

        #更新论坛版块内容 pre_forum_forum
        lastpost = '%s	%s	%s	%s' % (tid, subject, unixtime, author)
        self.cursor.execute('update pre_forum_forum set threads = threads + 1, posts=posts+1, todayposts=todayposts+1, lastpost=%s where fid=%s', (lastpost,fid))

        #更新用户统计数据 pre_common_member_count
        self.cursor.execute('update pre_common_member_count set posts=posts+1, threads=threads+1 where uid=%s', (authorid,))

    #网易新闻
    def parse_163_news(self, response):
        hxs = HtmlXPathSelector(response)
        url = response.url
        urlmd5 = md5(url)
        self.cursor.execute('select url from url_history where urlmd5=%s', (urlmd5,))
        r = self.cursor.fetchone()
        if  r:
            print 'scraped'
            return None

        #设置用户、版块、类别等信息 uid:12 fid:41
        uid = 12
        fid = 71
        typeid = 0

        title = ''.join(hxs.select(u'//h1[@id="h1title"]/text()').extract()).encode('utf8')
        content = '<br/>'.join(hxs.select(u'//div[@id="endText"]/p').extract()).encode('utf8')

        if title:
            print '163news'

            author =  '资讯小编'
            d1 = datetime.datetime.now(tz)
            #d3 = d1 + datetime.timedelta(days = random.randint(-20, 0))
            d3 = d1 + datetime.timedelta(hours = random.randint(-2, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')
            self.post(title, content, fid, uid, author, posttime, typeid, 1, -1)

            #记录痕迹
            self.cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))

    #网易房产
    def parse_163_house(self, response):
        hxs = HtmlXPathSelector(response)
        url = response.url
        urlmd5 = md5(url)
        self.cursor.execute('select url from url_history where urlmd5=%s', (urlmd5,))
        r = self.cursor.fetchone()
        if  r:
            print 'scraped'
            return None

        #设置用户、版块、类别等信息 uid:12 fid:41
        uid = 12
        fid = 38
        typeid = 0

        title = ''.join(hxs.select(u'//h1[@id="h1title"]/text()').extract()).encode('utf8')
        content = '<br/>'.join(hxs.select(u'//div[@id="endText"]/p').extract()).encode('utf8')

        if title:
            print '163news'

            author =  '资讯小编'
            d1 = datetime.datetime.now(tz)
            #d3 = d1 + datetime.timedelta(days = random.randint(-20, 0))
            d3 = d1 + datetime.timedelta(hours = random.randint(-2, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')
            self.post(title, content, fid, uid, author, posttime, typeid, 1, -1)

            #记录痕迹
            self.cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))