#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
USER_TOKEN = ''
USER_SECRET = ''
RETURN_URL = ''

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
    title = 'Wholesales Best shown L-carnitine 360 slimming coffee'
    summary = 'Coffee is a fast-acing,fat-burning beverage,to be effective for weight loss with no side effect and dependency,It is one of the best seller brand with high repution from its consumers.Weight loss made simple and rapid you will lose excess pounds and become slimmer that you can see and feel in just 6days.It is tasty and refreshing'

    submitted_url = 'http://www.freeb2bmarket.com/product/993622/best-shown-l-carnitine-360-slimming-coffee.html'
    submitted_image_url = 'http://www.freeb2bmarket.com/upload/2014_02_11_08_09_57_13_250x250.jpg'
    description = ''

    application.submit_group_post(groupid, title, summary, submitted_url, submitted_image_url, '', summary)
    i = i + 1