#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from settings import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

#print dir(application)#.get_profile()

#groups = [(6589270,'test group')]
#group = random.choice(groups)

posts = application.get_posts(6589270,params={'count':'10000'})['values']
posts_id = [p['id'] for p in posts]

postid = posts_id[1]
application.like_post(postid)