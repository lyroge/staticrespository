import tornado.ioloop
import tornado.web
from tornado import template
from pyquery import PyQuery as pq
import urllib 
from linkedin import linkedin
from const.db import HOST,USER,PASSWD,DB
import MySQLdb.cursors

API_KEY = '75c0f9yf94xtzf'
API_SECRET = 'EU4UtGEVIzEO6zh9'
RETURN_URL = 'http://localhost:8888/share'

authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
auth_url =  authentication.authorization_url
app = linkedin.LinkedInApplication(authentication)

conn = MySQLdb.connect(host=HOST,user=USER,passwd=PASSWD,db=DB,cursorclass=MySQLdb.cursors.DictCursor)
conn.set_character_set('utf8')
cursor=conn.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		self.redirect(auth_url)

class ShareHandler(tornado.web.RequestHandler):
	def get(self):
		global authentication
		code = self.get_argument('code')

		if not authentication.authorization_code:
			authentication.authorization_code = code
			authentication.get_access_token()

		#pid = self.get_argument('pid')
		cursor.execute('select * from product where id=4650')
		product=cursor.fetchone()

		groups = [(a['group']['id'],a['group']['name']) for a in app.get_memberships(params={'count':'1000'})['values']]
		self.render('share.html', groups=groups,product=product)

	def post(self):
		dtitle=self.get_argument('dtitle')
		summary=self.get_argument('summary')
		submitted_url=self.get_argument('url')
		submitted_image_url=self.get_argument('imageurl')

		ctitle=self.get_argument('ctitle')
		desc=self.get_argument('desc')

		groupids=self.get_argument('groupids').split(',')
		for groupid in groupids:
			app.submit_group_post(groupid, dtitle, summary, submitted_url, submitted_image_url, ctitle, desc)

'''
application = tornado.web.Application([
	(r"/login", LoginHandler),
	(r"/share", ShareHandler),
])

if __name__ == "__main__":
	application.listen(8989)
	tornado.ioloop.IOLoop.instance().start()
'''