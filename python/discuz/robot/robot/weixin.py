# -- coding:utf-8 --

import re,time,datetime,hashlib,urllib2,pytz,random
import MySQLdb, MySQLdb.cursors
from pyquery import PyQuery as pq
from const.db import HOST,USER,PASSWD,DB

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

#数据库对象
conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
conn.set_character_set('utf8')
cursor=conn.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

#提交主题到dz
def post(subject, content, fid, authorid, author, posttime, typeid, htmlon=0, bbcodeoff=0):
    #插入主题
    unixtime = timestamp(posttime)
    param = (fid, author, authorid, subject, unixtime, unixtime, author, typeid, random.randint(8, 51))
    cursor.execute('INSERT INTO pre_forum_thread(fid, author, authorid, subject, dateline, lastpost, lastposter, typeid, views) values(%s, %s, %s, %s, %s, %s, %s, %s, %s)', param)
    tid = cursor.lastrowid

    #获取pid pre_forum_post_tableid
    cursor.execute('INSERT INTO pre_forum_post_tableid(pid) values(%s)', ('0',))
    pid = cursor.lastrowid

    #插入主题内容 pre_forum_post [htmlon=1, bbcodeoff=-1] 允许帖子中html代码
    param = (pid, fid, tid, author, authorid, subject, unixtime, content, '127.0.0.1', '22622', htmlon, bbcodeoff)
    cursor.execute('INSERT INTO pre_forum_post (pid, fid, tid, author, authorid, subject, dateline, message, useip, port, htmlon, bbcodeoff) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', param)

    #更新论坛版块内容 pre_forum_forum
    lastpost = '%s  %s  %s  %s' % (tid, subject, unixtime, author)
    cursor.execute('update pre_forum_forum set threads = threads + 1, posts=posts+1, todayposts=todayposts+1, lastpost=%s where fid=%s', (lastpost,fid))

    #更新用户统计数据 pre_common_member_count
    cursor.execute('update pre_common_member_count set posts=posts+1, threads=threads+1 where uid=%s', (authorid,))

#抓取微信消息
url = 'http://weixin.sogou.com/gzhjs?cb=sogou.weixin.gzhcb&openid=oIWsFtyz988efIV56tzisxgOIOfs&page=1&t=1403513177899'
r = urllib2.urlopen(url)
content = r.read()
reg = re.compile(r'<url><!\[CDATA\[(.*?)\]\]')

result = reg.findall(content)
result = result[:3]
for u in result:
    print u
    urlmd5 = md5(u)
    cursor.execute('select url from url_history where urlmd5=%s', (urlmd5,))
    r = cursor.fetchone()
    if  r:
         print 'scraped'
    else:
        d = pq(url=u)
        title = d("h1").html().encode('utf8')
        content = d('#img-content').html().encode('utf8')
        typename = d('p.activity-info').text().encode('utf8')

        if '' in typename:
            print 'right'
            fid, uid = 39, 2
            author =  'abc'
            d1 = datetime.datetime.now(tz)
            #d3 = d1 + datetime.timedelta(days = random.randint(-20, 0))
            d3 = d1 + datetime.timedelta(hours = random.randint(-4, 0))
            d3 = d3 + datetime.timedelta(minutes = random.randint(-30, 12))
            d3 = d3 + datetime.timedelta(seconds = random.randint(-45, 2))
            posttime = d3.strftime('%Y-%m-%d %H:%M')
            post(title, content, fid, uid, author, posttime, 0, 1, -1)

            #记录痕迹
            cursor.execute('insert url_history(url, urlmd5) values(%s, %s)', (url, urlmd5))

cursor.close()
conn.close()