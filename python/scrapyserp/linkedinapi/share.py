#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from settings import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

#print dir(application)#.get_profile()

groups = [(a['group']['id'],a['group']['name']) for a in application.get_memberships(params={'count':'1000'})['values']]

#groups = [(115178,'test group')]
#group = random.choice(groups)

i = 1
for group in groups:
    groupid = group[0]
    print i

    #post a group discuss
    title = 'We are Manufacturer of film face plywood,commercial plywood,melamine plywood'
    summary = 'XUZHOU XINYU  Wood Co., Ltd., founded in 2003, covers an area of 36 acres, standardized plant area of 24,000 square meters, has advanced auto-production line six, and the set of the original double-sided sanding machine, glue and other advanced reactor equipment, to undertake a variety of sizes of the film faced plywood, plywood.'

    submitted_url = 'http://www.freeb2bmarket.com/company/xuzhou-xinyu-wood-ltd.html'
    submitted_image_url = 'http://www.freeb2bmarket.com/upload/2014_02_17_09_17_21_DSC00892.JPG'
    description = '''XUZHOU XINYU  Wood Co., Ltd., founded in 2003, covers an area of 36 acres, standardized plant area of 24,000 square meters, has advanced auto-production line six, and the set of the original double-sided sanding machine, glue and other advanced reactor equipment, to undertake a variety of sizes of the film faced plywood, plywood. our strong production capacity. Since the establishment of the day, the company had not stopped the moment the pace of innovation. For years, the company uphold: integrity, innovation, cooperation and win-win "in business philosophy of innovation throughout all aspects of business management to enable enterprises to gradually grow and develop'''

    time.sleep(2)
    application.submit_group_post(groupid, title, summary, submitted_url, submitted_image_url, 'XUZHOU XINYU  Wood Co., Ltd.', summary)
    i = i + 1