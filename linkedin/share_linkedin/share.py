import tornado.ioloop
import tornado.web
from tornado import template
from pyquery import PyQuery as pq
import urllib 
from linkedin import linkedin

API_KEY = ''
API_SECRET = ''
RETURN_URL = 'http://localhost:8989/share'

authentication = linkedin.LinkedInAuthentication(API_KEY, API_SECRET, RETURN_URL, linkedin.PERMISSIONS.enums.values())
auth_url =  authentication.authorization_url
app = linkedin.LinkedInApplication(authentication)

class LoginHandler(tornado.web.RequestHandler):
	def get(self):
		capters = {}
		self.redirect(auth_url)

class ShareHandler(tornado.web.RequestHandler):
	def get(self):
		global authentication
		code = self.get_argument('code')

		if not authentication.authorization_code:
			authentication.authorization_code = code
			authentication.get_access_token()

		groups = [(a['group']['id'],a['group']['name']) for a in app.get_memberships(params={'count':'1000'})['values']]
		self.render('index.html', groups=groups)

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

application = tornado.web.Application([
	(r"/login", LoginHandler),
	(r"/share", ShareHandler),
])

if __name__ == "__main__":
	application.listen(8989)
	tornado.ioloop.IOLoop.instance().start()