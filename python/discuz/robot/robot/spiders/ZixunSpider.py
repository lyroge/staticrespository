# -- coding:utf-8 --

import re, os, random, datetime, time, hashlib
import MySQLdb, MySQLdb.cursors

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.shell import inspect_response

from robot.const.db import HOST,USER,PASSWD,DB

def md5(s):
    return hashlib.md5(s).hexdigest()

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
        #易畅二手市场
        Rule(SgmlLinkExtractor(unique=True,allow=("\?page=[1-5]"))),
        Rule(SgmlLinkExtractor(unique=True,allow=('xiangxi.asp\?id=\d+', )), callback='parse_item')
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

    def post(self, subject, content, fid, authorid, author, posttime, typeid):
        #插入主题
        unixtime = timestamp(posttime)  
        param = (fid, author, authorid, subject, unixtime, unixtime, author, typeid)
        self.cursor.execute('INSERT INTO pre_forum_thread(fid, author, authorid, subject, dateline, lastpost, lastposter, typeid) values(%s, %s, %s, %s, %s, %s, %s, %s)', param)
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

    def parse_item(self, response):
        hxs = HtmlXPathSelector(response)
        url = response.url
        urlmd5 = md5(url)
        self.cursor.execute('select url from url_history where urlmd5=%s', (urlmd5,))
        r = self.cursor.fetchone()
        if  r:
            return None

        #设置用户、版块、类别等信息
        uid = 2
        fid = 39
        typeid = 0

        typename = ''.join(hxs.select(u'//td[contains(text(),"供求类别")]/following-sibling::td/text()').extract()).encode('utf8')
        title = ''.join(hxs.select(u'//td[contains(text(),"信息主题")]/following-sibling::td/text()').extract()).encode('utf8')
        username = ''.join(hxs.select(u'//td[contains(text(),"联系姓名")]/following-sibling::td/text()').extract()).encode('utf8')
        telphone = ''.join(hxs.select(u'//td[contains(text(),"联系电话")]/following-sibling::td/text()').extract()).encode('utf8')

        content = ''.join(hxs.select(u'//p[contains(text(),"详细介绍")]/parent::td/following-sibling::td/table[2]/descendant-or-self::text()').extract()).encode('utf8')
        content = content + "\r\n[b]联系人：[/b]" + username
        content = content + "\r\n[b]联系电话：[/b]" + telphone
        content = content + "\r\n\r\n\r\n\r\n[color=red][b]联系时请说明来自平谷资讯网 http://bbs.pgzixun.com [/b][/color]"


        if '供应' in typename:
            typeid = 2
        else:
            typeid = 1

        if title:
            print title

            author =  username if username else '资讯小编'
            d1 = datetime.datetime.now()
            d3 = d1 + datetime.timedelta(days = random.randint(-20, 0))
            d3 = d3 + datetime.timedelta(hours = random.randint(-30, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')
            self.post(title, content, fid, uid, author, posttime, typeid)

            #记录痕迹
            self.cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))