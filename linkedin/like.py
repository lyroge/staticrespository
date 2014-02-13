#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from settings import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)


groups = [(a['group']['id'],a['group']['name']) for a in application.get_memberships(params={'count':'1000'})['values']]

group = random.choice(groups)
group = (6589270,'test group')

groupid = group[0]

posts = application.get_posts(groupid,params={'count':'10000'})['values']
posts_id = [p['id'] for p in posts]


print posts_id