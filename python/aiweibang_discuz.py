# -*- coding: UTF-8 -*-

import re
import time
import datetime
import pytz
import random
import MySQLdb
import MySQLdb.cursors
from pyquery import PyQuery as pq
from selenium import webdriver


url_base = 'http://www.aiweibang.com'
url_template = 'http://www.aiweibang.com/u/18393?page=%s'


tz = pytz.timezone('Asia/Shanghai')


cursor = None
HOST = ''
USER = ''
PASSWD = ''
DB = ''


class DiscuzMysqlConnectFailedException(Exception):
    pass


class Discuz(object):
    """ Discuz论坛数据表操作类
    """

    def __init__(self, host, user, passwd, db):
        try:
            conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, cursorclass=MySQLdb.cursors.DictCursor)
        except DiscuzMysqlConnectFailedException, e:
            raise e
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        self.conn = conn
        self.cursor = cursor

    def _make_timestamp(str):
        if not str:
            a = datetime.datetime.now(tz)
        else:
            a = datetime.datetime.strptime(str, '%Y-%m-%d %H:%M')
        t = time.mktime(a.timetuple())
        return t

    def post(self, subject, content, fid, authorid, author, posttime, typeid, htmlon=1, bbcodeoff=0):
        """ 发布一个帖子

        args:
            subject: 帖子题目
            content: 帖子内容
            fid: 版块id
            authorid: 发布人id
            author: 发布人名称
            posttime: 发布时间（时间戳）
            typeid: 类别id
            htmlon: 允许HTML内容
            bbcodeoff: 允许bbcode内容
        """

        # 发布一个主题
        unixtime = self._make_timestamp(posttime)
        param = (fid, author, authorid, subject, unixtime,
                 unixtime, author, typeid, random.randint(8, 51))
        self.cursor.execute('INSERT INTO forum_thread(fid, author, authorid, subject, dateline, lastpost, lastposter, typeid, views) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', param)
        tid = self.cursor.lastrowid

        # 获取新发布帖子的id
        self.cursor.execute('INSERT INTO forum_post_tableid(pid) values(%s)', ('0',))
        pid = self.cursor.lastrowid

        # 发布帖子内容 [htmlon=1, bbcodeoff=-1] 允许帖子中html代码
        param = (pid, fid, tid, author, authorid, subject, unixtime, content, '127.0.0.1', '22622', htmlon, bbcodeoff)
        cursor.execute('INSERT INTO forum_post (pid, fid, tid, author, authorid, subject, dateline, message, useip, port, htmlon, bbcodeoff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', param)

        # 更新论坛版块内容
        lastpost = '%s  %s    %s  %s' % (tid, subject, unixtime, author)
        cursor.execute('update forum_forum set threads=threads + 1, posts=posts+1, todayposts=todayposts+1, lastpost=%s where fid=%s', (lastpost, fid))

        # 更新用户统计数据 common_member_count
        cursor.execute('update common_member_count set posts=posts+1, threads=threads+1 where uid=%s', (authorid,))

discuz = Discuz(HOST, USER, PASSWD, DB)

PROXY_PhantomJS = '/usr/local/bin/phantomjs'
driver = webdriver.PhantomJS(PROXY_PhantomJS)
driver.set_page_load_timeout(10)

for i in range(1, 2):
    url = url_template % i
    d = pq(url=url)
    title_dom_list = d(".msg-list .title a")
    for dom in title_dom_list:
        d = pq(dom)
        title = d.text().encode('utf8')
        print title
        href = d.attr('href')

        print 'get detail page source...'
        try:
            driver.get(url_base + href)
        except Exception as e:
            print str(e)
            continue
        page_source = driver.page_source
        dd = pq(page_source)
        body = dd('.page-content').outerHtml()
        body = body.replace('style="height: 500px; overflow: hidden;"', '')

        # 将html中的lazy图片处理正常加载
        body = re.sub('<img(.*?)(original)(.*?)>', '<img\\1src\\3>', body)

        print 'post content to discuz...'
        posttime = datetime.datetime.now(tz)
        posttime = posttime.strftime('%Y-%m-%d %H:%M')
        discuz.post(title, body, 2, 269, '平谷资讯小编', posttime, 0, htmlon=1)
