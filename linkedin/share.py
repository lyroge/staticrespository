#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from settings import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

#print dir(application)#.get_profile()

groups = [(a['group']['id'],a['group']['name']) for a in application.get_memberships(params={'count':'1000'})['values']]

groups = [(115178,'test group')]
#group = random.choice(groups)

i = 1
for group in groups:
    groupid = group[0]
    print i

    #post a group discuss
    title = 'Looking for BUYERS about T-shirts Polo Shirts Tank-Tops'
    summary = 'We are the manufacturer of Shirts, main products :T-shirts, Polo Shirts, Tank-Tops'

    submitted_url = 'http://www.freeb2bmarket.com/company/brand-tex-corporation-bangladesh.html'
    submitted_image_url = 'http://www.freeb2bmarket.com/upload/2014_02_12_05_22_40_02.png'
    description = 'Looking for BUYERS about T-shirts, Polo Shirts, Tank-Tops. We make Shirt, Jeans, Coverall, Bottoms and Jackets, Trouser in all kind of materials.'

    time.sleep(2)
    application.submit_group_post(groupid, title, summary, submitted_url, submitted_image_url, 'BRAND TEX Corporation Bangladesh', summary)
    i = i + 1