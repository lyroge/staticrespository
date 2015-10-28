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

    def _make_timestamp(self, str):
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
        self.cursor.execute('INSERT INTO forum_post (pid, fid, tid, author, authorid, subject, dateline, message, useip, port, htmlon, bbcodeoff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', param)

        # 更新论坛版块内容
        lastpost = '%s  %s    %s  %s' % (tid, subject, unixtime, author)
        self.cursor.execute('update forum_forum set threads=threads + 1, posts=posts+1, todayposts=todayposts+1, lastpost=%s where fid=%s', (lastpost, fid))

        # 更新用户统计数据 common_member_count
        self.cursor.execute('update common_member_count set posts=posts+1, threads=threads+1 where uid=%s', (authorid,))

discuz = Discuz(HOST, USER, PASSWD, DB)

PROXY_PhantomJS = '/usr/local/bin/phantomjs'
driver = webdriver.PhantomJS(PROXY_PhantomJS)
driver.set_page_load_timeout(30)

for i in range(1, 2):
    url = url_template % i
    d = pq(url=url)
    msg_items = d(".msg-list .msg-item")
    """
    <div class="msg-item" style="">
        <div class="date">
            <span class="day">27</span>
            <span class="month">15-10</span>
        </div>
        <div class="info">
            <div class="title">
                <a title="北京住房公积金管理中心2015年公开招聘工作人员公告（含平谷地区）" href="/yuedu/60548236.html" target="_blank">北京住房公积金管理中心2015年公开招聘工作人员公告（含平谷地区）</a>
            </div>
            <div class="summary">
                <div class="pic">
                    <div class="picinner">
                        <a title="北京住房公积金管理中心2015年公开招聘工作人员公告（含平谷地区）" href="/yuedu/60548236.html" target="_blank">
                            <img src="http://awb.img1.xmtbang.com/cover201510/20151027/thumb/ac206bdcaaa94a95944a9e36631c31cd.jpg" onerror="this.parentNode.parentNode.parentNode.parentNode.removeChild(this.parentNode.parentNode.parentNode)" original="http://awb.img1.xmtbang.com/cover201510/20151027/thumb/ac206bdcaaa94a95944a9e36631c31cd.jpg" alt="北京住房公积金管理中心2015年公开招聘工作人员公告（含平谷地区）" style="display: inline;">
                        </a>
                    </div>
                </div>
                <div class="text">点上方“平谷资讯" 免费订阅 惊喜不断！平 谷 生 活 一 手 掌 握平谷地区最具影响力微信平台商家合作回</div>
            </div>
            <div class="clear h"></div>
            <div class="ifooter">
                <span class="text">昨天</span>
                <span class="fav-operate">
                    <a class="favarticle " href="javascript:;" data-articleid="60548236">收藏，稍后阅读</a>
                    <a class="unfavarticle undis" href="http://u.aiweibang.com/fav/article" target="_blank">已收藏</a>
                </span>
            </div>
        </div>
    </div>
    """
    for dom in msg_items:
        d = pq(dom)

        # date
        date_span_dom = d.find('.date .day')
        date = date_span_dom.text().encode('utf8')

        # title
        title_a_dom = d.find('.title a')
        title = title_a_dom.text().encode('utf8')
        print date, title
        href = title_a_dom.attr('href')

        print 'get detail page source...'
        try:
            driver.get(url_base + href)
        except Exception as e:
            print str(e)
        print 'done'
        page_source = driver.page_source
        dd = pq(page_source)
        body = dd('.page-content').outerHtml()
        body = body.replace('style="height: 500px; overflow: hidden;"', '')

        # 将html中的lazy图片处理正常加载
        body = re.sub('<img(.*?)(original)(.*?)>', '<img\\1src\\3>', body)

        print 'post content to discuz...'
        posttime = datetime.datetime.now(tz)
        posttime = posttime.strftime('%Y-%m-%d %H:%M')
        # discuz.post(title, body, 2, 269, '平谷资讯小编', posttime, 0, htmlon=1)
