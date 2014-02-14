#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from settings import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

groups = [(a['group']['id'],a['group']['name']) for a in application.get_memberships(params={'count':'1000'})['values']]



for i in range(0,50):
	group = random.choice(groups)
	#group = (6589270,'test group')
	print group
	groupid = group[0]

	#get all posts
	posts = application.get_posts(groupid,params={'count':'10000'})['values']
	posts_id = [p['id'] for p in posts]

	application.like_post(random.choice(posts_id))
	t = random.choice([21,5,13,4,10])
	time.sleep(t)

'''
	posts_id = [p['id'] for p in posts]

	#like 10
	c = 10 if len(posts_id) > 10 else len(posts_id)
	for i in range(0,c):
		print 'like %d' % i
		application.like_post(random.choice(posts_id))
		t = random.choice([1,2,3,4])
		time.sleep(t)'''