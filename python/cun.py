# -*- coding: UTF-8 -*-

import os
import urllib
import time
import threading
from Queue import Queue

from pyquery import PyQuery as pq

# 每集文件的详情url
url_template = "http://cswanda.com/weixin/game1/xiangcun/cun%s.html"

# 用线程安全的队列
q = Queue(maxsize=70)

# 共65集文件
for i in range(1, 66, 1):
    q.put(i)

# 配置启动线程数量
THREAD_COUNT = 5


class downloader(threading.Thread):
    """ 多线程下载器
    """

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while q.qsize() > 0:
            i = q.get()
            url = url_template % i
            d = pq(url=url)
            src = d(".MacPlayer iframe").attr('src')

            d = pq(url=src)
            video_url = d("source").attr('src')

            name = '%s/第%s集.mp4' % (dirname, i)
            print '开始下载%s...' % name
            urllib.urlretrieve(video_url, name)
            print '下载完毕%s...' % name


if __name__ == "__main__":
    # 运行当前目录创建文件夹
    # 将每一集文件放到文件夹下面
    dirname = "乡村爱情故事8"
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    thread_list = []
    for i in range(THREAD_COUNT):
        t = downloader()
        thread_list.append(t)
        t.start()

        # 线程间延迟1s启动时间
        time.sleep(1)

    for t in thread_list:
        t.join()

    print '全部下载完毕 ^_^'
