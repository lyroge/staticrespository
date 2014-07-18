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

#过滤特殊字符
def filter_spechar(s):
    s = s.replace('█', '')
    s = s.replace('◆', '')
    s = s.replace('★', '')
    s = s.replace('●', '')
    s = s.replace('▲', '')
    s = s.replace('▼', '')
    s = s.replace('&nbsp;', '')
    return s.strip()

class ZixunSpider(CrawlSpider):
    name = "Zixun"
    allowed_domains = []

    start_urls = ['http://www.echang.cn/house/lx.asp?lx=0','http://www.echang.cn/house/lx.asp?lx=1','http://www.echang.cn/house/lx.asp?lx=2','http://www.echang.cn/house/lx.asp?lx=3','http://www.echang.cn/2shou/?page=1','http://www.echang.cn/job/qy.asp?gw=&lx=&sj=365&gz=&xl=&key=&page=1']

    rules = (
        #易畅二手市场
        Rule(SgmlLinkExtractor(unique=True,allow=("\?page=[1]$"))),
        Rule(SgmlLinkExtractor(unique=True,allow=('/2shou/xiangxi.asp\?id=\d+$', )), callback='parse_echang_ershou'),

        #易畅招聘
        Rule(SgmlLinkExtractor(unique=True,allow=('/job/zhaopin.asp\?id=\d+$', )), callback='parse_echang_zhaopin'),

        #易畅房屋买卖租赁 每日取一条最新的
        Rule(SgmlLinkExtractor(unique=True,allow=('/house/xiangxi.asp\?id=\d+$'),restrict_xpaths=('/html/body/table[5]/tr[2]/td[2]/table[2]/tr/td[1]/table[3]/tr[1]/td[3]/a | /html/body/table[5]/tr[2]/td[2]/table[3]/tr/td[1]/table[3]/tr[1]/td[3]/a | /html/body/table[5]/tr[2]/td[2]/table[6]/tr/td[1]/table[3]/tr[1]/td[2]/a | /html/body/table[5]/tr[2]/td[2]/table[6]/tr/td[3]/table[3]/tr[1]/td[2]/a',)), callback='parse_echang_fangchan')
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

    #易畅二手
    def parse_echang_ershou(self, response):
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
        fid = 41
        typeid = 0

        typename = ''.join(hxs.select(u'//td[contains(text(),"供求类别")]/following-sibling::td/text()').extract()).encode('utf8')
        title = ''.join(hxs.select(u'//td[contains(text(),"信息主题")]/following-sibling::td/text()').extract()).encode('utf8')
        username = ''.join(hxs.select(u'//td[contains(text(),"联系姓名")]/following-sibling::td/text()').extract()).encode('utf8')
        telphone = ''.join(hxs.select(u'//td[contains(text(),"联系电话")]/following-sibling::td/text()').extract()).encode('utf8')

        content = ''.join(hxs.select(u'//p[contains(text(),"详细介绍")]/parent::td/following-sibling::td/table[2]/descendant-or-self::text()').extract()).encode('utf8')
        content = content + "\r\n[b]联系人：[/b]" + username
        content = content + "\r\n[b]联系电话：[/b]" + telphone
        content = content + "\r\n\r\n\r\n\r\n[color=red][b]联系时请说明来自平谷资讯网 http://www.pgzixun.com [/b][/color]"

        if '供应' in typename:
            typeid = 4
        else:
            typeid = 3

        if title:
            print 'ershou'

            author =  username if username else '资讯小编'
            d1 = datetime.datetime.now(tz)
            #d3 = d1 + datetime.timedelta(days = random.randint(-20, 0))
            d3 = d1 + datetime.timedelta(hours = random.randint(-4, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')
            self.post(title, content, fid, uid, author, posttime, typeid)

            #记录痕迹
            self.cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))

    #易畅招聘
    def parse_echang_zhaopin(self, response):
        hxs = HtmlXPathSelector(response)
        url = response.url
        urlmd5 = md5(url)
        self.cursor.execute('select url from url_history where urlmd5=%s', (urlmd5,))
        r = self.cursor.fetchone()
        if  r:
            print 'scraped'
            return None

        #设置用户、版块、类别等信息 uid:12 fid:42
        uid = 12
        fid = 42
        typeid = 0

        title = ''.join(hxs.select(u'//font[contains(text(),"招聘职位：")]/parent::td/following-sibling::td/descendant-or-self::text()').extract()).encode('utf8')
        xueli = ''.join(hxs.select(u'//td[contains(text(),"学历要求：")]/following-sibling::td/text()').extract()).encode('utf8')
        xinzi = ''.join(hxs.select(u'//td[contains(text(),"提供月薪：")]/following-sibling::td/text()').extract()).encode('utf8')
        zhize = ''.join(hxs.select(u'//td[contains(text(),"招聘备注：")]/following-sibling::td/text()').extract()).encode('utf8')

        danwei = ''.join(hxs.select(u'//td[contains(text(),"单位名称：")]/following-sibling::td/text()').extract()).encode('utf8')
        dianhua = ''.join(hxs.select(u'//td[contains(text(),"联系电话：")]/following-sibling::td/text()').extract()).encode('utf8')
        intro = ''.join(hxs.select(u'//td[contains(text(),"公司介绍：")]/following-sibling::td/text()').extract()).encode('utf8')


        content = "[b]招聘职位：[/b]" + title
        content = content + "\r\n[b]学历要求：[/b]" + xueli
        content = content + "\r\n[b]提供月薪：[/b]" + xinzi
        content = content + "\r\n[b]岗位职责[/b]\r\n" + zhize

        content = content + "\r\n\r\n[b]单位名称[/b]\r\n" + danwei
        content = content + "\r\n\r\n[b]联系电话[/b]\r\n" + dianhua
        content = content + "\r\n\r\n[b]公司介绍[/b]\r\n" + intro

        content = content + "\r\n\r\n\r\n[color=red][b]联系时请说明来自平谷资讯网 http://www.pgzixun.com [/b][/color]"

        if title:
            print 'zhaopin'

            author =  '招聘编辑'
            d1 = datetime.datetime.now(tz)
            #d3 = d1 + datetime.timedelta(days = random.randint(-6, 0))
            d3 = d1 + datetime.timedelta(hours = random.randint(-4, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')
            self.post(title, content, fid, uid, author, posttime, typeid)

            #记录痕迹
            self.cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))

    #易畅房产
    def parse_echang_fangchan(self, response):
        hxs = HtmlXPathSelector(response)
        url = response.url
        urlmd5 = md5(url)
        self.cursor.execute('select url from url_history where urlmd5=%s', (urlmd5,))
        r = self.cursor.fetchone()
        if  r:
            print 'scraped'
            return None

        #设置用户、版块、类别等信息 uid:12 fid:43
        uid = 12
        fid = 43
        typeid = 0

        title = ''.join(hxs.select(u'//td[contains(text(),"具体位置")]/following-sibling::td/text()').extract()).replace(u'\xa0', u'').encode('utf8')
        lb = ''.join(hxs.select(u'//td[contains(text(),"所属社区")]/preceding-sibling::td[1]/text()').extract()).replace(u'\xa0', u'').encode('utf8')
        mark = '\r\n'.join(hxs.select(u'//td[contains(text()," 注")]//following-sibling::td/text()').extract()).replace(u'\xa0', u'').encode('utf8')
        username = ''.join(hxs.select(u'//td[starts-with(text(),"姓")]//following-sibling::td[position()=1]/text()').extract()).encode('utf8')
        telephone = ''.join(hxs.select(u'//td[contains(text(),"联系电话")]//following-sibling::td[position()=1]/text()').extract()).encode('utf8')
        mobile = ''.join(hxs.select(u'//td[contains(text(),"联系手机")]//following-sibling::td[position()=1]/text()').extract()).encode('utf8')

        content = mark
        content = content + "\r\n\r\n[b]联系电话：[/b]" + telephone
        content = content + "\r\n[b]联系手机：[/b]" + mobile
        content = content + "\r\n[b]联系人：[/b]" + username

        content = content + "\r\n\r\n\r\n\r\n[color=red][b]联系时请说明来自平谷资讯网 http://www.pgzixun.com [/b][/color]"
        content = content

        title = filter_spechar(title)
        content = filter_spechar(content)
        lb = filter_spechar(lb)

        type_dic = {'房屋出租':5, '房屋求租':6, '房屋出售':7, '房屋求购':8}
        typeid = type_dic[lb]


        if title:
            print 'fangchan'

            author =  username if username else '房产编辑'
            d1 = datetime.datetime.now(tz)
            #d3 = d1 + datetime.timedelta(days = random.randint(-6, 0))
            d3 = d1 + datetime.timedelta(hours = random.randint(-4, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')

            self.post(title, content, fid, uid, author, posttime, typeid)

            #记录痕迹
            self.cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))