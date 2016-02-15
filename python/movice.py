# -*- coding: utf-8 -*-
"""
爬取cswanda网站电影信息
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
返回数据结构包括电影基本信息和聚集信息：
[
    {
      'name': '电影名称',
      'cover': '电影封面',
      'lasttime': '最后更新时间',
      'tag': '标签',
      'url': '网址',
      'children': [
            {
                'name': '剧集',
                'video_url': '视频地址',
                'url': '网址'
            }
      ]
    },
]
"""

import time
import random
import sys
import re
from urlparse import urljoin
from functools import partial

import requests
import MySQLdb
import MySQLdb.cursors
from pyquery import PyQuery as _pq

reload(sys)
sys.setdefaultencoding('utf8')


class DB(object):
    """ Discuz论坛数据表操作类
    """

    def __init__(self, host, user, passwd, db):
        try:
            conn = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, cursorclass=MySQLdb.cursors.DictCursor)
        except Exception, e:
            raise e
        conn.set_character_set('utf8')
        cursor = conn.cursor()
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        self.conn = conn
        self.cursor = cursor

    def import_data(self, items):

        for item in items:
            name = item['name']
            cover = item['cover']
            lasttime = item['lasttime']
            tag = item['tag']
            url = item['url']
            children = item['children']

            # 发布一个电影
            param = (name, cover, lasttime, tag, url)
            self.cursor.execute('insert into video(name, cover, lasttime, tag, url) values(%s, %s, %s, %s, %s)', param)
            video_id = self.cursor.lastrowid

            for c in children:
                name = c['name']
                url = c['url']
                video_url = c['video_url']

                # 发布剧集
                param = (name, url, video_url, video_id)
                self.cursor.execute('insert into video_child(name, url, video_url, video_id) values(%s, %s, %s, %s)', param)

        self.conn.commit()
        self.cursor.close()
        self.conn.close()


def main():
    cswanda_url = "http://cswanda.com/weixin/game1/move.html#rd"
    headers = {
        "User-Agent": "Mozilla/5.0  micromessenger  (iPhone; CPU iPhone OS 8_0 like Mac OS X)",
        "Referer": "http://www.cswanda.com/weixin/game1/20160212fuxing.html",
        "Cookie": "Hm_lvt_231f28366e4ba8a5d75304ebe893f692=1452923662"
    }

    # 创建_pq的偏函数
    pq = partial(_pq, headers=headers, encoding='utf8')

    # 抓取主页全部电影信息
    d = pq(url=cswanda_url)
    li_dom_list = d(".tb_a ul li")

    # 保存获取的电影结构化数据
    items = []
    for li_dom in li_dom_list:
        li = d(li_dom)

        # 获取电影的基本信息
        title = li.find(".sTit").text()
        print title

        # 电影相对链接
        href = li.find("a").attr("href")
        if not href.startswith("./"):
            continue
        url = urljoin(cswanda_url, href)

        # 封面图片地址
        src = li.find('img').attr("data-echo")

        # 标签及更新时间信息
        lasttime = li.find(".sDes").text()
        tag = li.find(".emHot").text()

        item = {
            'name': title,
            'cover': src,
            'lasttime': lasttime,
            'tag': tag,
            'url': url,
            'children': []
        }

        # 获取视频的url地址
        # url为播放视频的地址
        # http://www.cswanda.com/weixin/game1/heke1.html
        def get_video_url(url):
            d = pq(url=url)
            src = d(".MacPlayer iframe").attr('src')
            if not src:
                return
            d = pq(url=src)
            video_url = d("source").attr('src')
            if not video_url:
                r = requests.get(url=src, headers=headers)
                r.encoding = 'utf8'
                body = r.text
                match = re.search("<source src=\"(.*?)\"", body)
                video_url = match.group(1)

            # 格式不正确，那么返回None
            if 'url' in video_url:
                return

            # r = requests.get(url=video_url, allow_redirects=False)
            # if r.status_code == 302:
            #     video_url = r.headers.get('location') or video_url

            # sleep_seconds = random.randint(1, 5)
            # time.sleep(sleep_seconds)
            return video_url

        # 获取电影剧集信息
        d2 = pq(url=url, encoding="gb2312")

        # 如果存在多部剧集，那么全部获取
        children_dom_list = d2("#dramaNumList li a")
        for children in children_dom_list:
            a = d2(children)
            title = a.text()
            href = a.attr('href')
            video_page_url = urljoin(url, href)
            video_url = get_video_url(video_page_url)
            if not video_url:
                continue
            item['children'].append({
                'name': title,
                'url': video_page_url,
                'video_url': video_url
            })

        # 如果没有多个剧集
        if not children_dom_list:
            video_url = get_video_url(url)
            item['children'].append({
                'name': title,
                'url': url,
                'video_url': video_url
            })
        items.append(item)

    # 导入数据到数据库
    db = DB('localhost', 'root', 'abc', 'test')
    db.import_data(items)

if __name__ == "__main__":
    main()
