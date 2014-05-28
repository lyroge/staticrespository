# -- coding:utf-8 --

import re, os, random, datetime, time
import MySQLdb, MySQLdb.cursors

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.shell import inspect_response

from robot.const.db import HOST,USER,PASSWD,DB

def timestamp(dtstr):
    if not dtstr:
        a = datetime.datetime.now()
    else:
        a=datetime.datetime.strptime(dtstr, '%Y-%m-%d %H:%M')
    t=time.mktime(a.timetuple())
    return t

class ZixunSpider(CrawlSpider):
    name = "Zixun"
    allowed_domains = []
    start_urls = ['http://www.echang.cn/2shou/?page=1']

    rules = (
        #Rule(SgmlLinkExtractor(unique=True,allow=("\?page=1"))),
        Rule(SgmlLinkExtractor(unique=True,allow=('xiangxi.asp\?id=207641', )), callback='parse_item')
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
        super(ZixunSpider, self).__init__()

    def post(self, subject, content, fid, authorid, author, posttime):
        #插入主题
        unixtime = timestamp(posttime)  
        param = (fid, author, authorid, subject, unixtime, unixtime, author)
        self.cursor.execute('INSERT INTO pre_forum_thread(fid, author, authorid, subject, dateline, lastpost, lastposter) values(%s, %s, %s, %s, %s, %s, %s)', param)
        tid = self.cursor.lastrowid

        #获取pid pre_forum_post_tableid
        self.cursor.execute('INSERT INTO pre_forum_post_tableid(pid) values(%s)', ('0',))
        pid = self.cursor.lastrowid

        #插入主题内容 pre_forum_post
        param = (pid, fid, tid, author, authorid, subject, unixtime, content, '127.0.0.1', '22622')
        self.cursor.execute('INSERT INTO pre_forum_post (pid, fid, tid, author, authorid, subject, dateline, message, useip, port) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', param)

        #更新论坛版块内容 pre_forum_forum
        lastpost = '%s  %s  %s  %s' % (tid, subject, unixtime, author)
        self.cursor.execute('update pre_forum_forum set threads = threads + 1, posts=posts+1, todayposts=todayposts+1, lastpost=%s where fid=%s', (lastpost,fid))

        #更新用户统计数据 pre_common_member_count
        self.cursor.execute('update pre_common_member_count set posts=posts+1, threads=threads+1 where uid=%s', (authorid,))
        print 'done'

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)

        uid = 2
        fid = 2
        title = ''.join(hxs.select('//td[contains(text(),"信息主题")]/following-sibling::td/text()').extract())
        content = ''.join(hxs.select('//p[contains(text(),"详细介绍")]/parent::td/following-sibling::td/table[2]/descendant-or-self::text()').extract())

        #print title
        self.post(title, content, fid, uid, '资讯小编', '')