#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from . import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

#print dir(application)#.get_profile()

groups = [(a['group']['id'],a['group']['name']) for a in application.get_memberships(params={'count':'1000'})['values']]

#groups = [(6589270,'test group')]
#group = random.choice(groups)

i = 1
for group in groups:
    groupid = group[0]
    print i

    #post a group discuss
    title = ''
    summary = ''

    submitted_url = ''
    submitted_image_url = ''
    description = ''

    time.sleep(2)
    application.submit_group_post(groupid, title, summary, submitted_url, submitted_image_url, '', summary)
    i = i + 1