#! /usr/bin/python2.7
# -- coding:utf-8 --

import random, time
from linkedin import linkedin
from settings import CONSUMER_KEY,CONSUMER_SECRET,USER_TOKEN,USER_SECRET,RETURN_URL

authentication = linkedin.LinkedInDeveloperAuthentication(CONSUMER_KEY, CONSUMER_SECRET,USER_TOKEN, USER_SECRET,RETURN_URL, linkedin.PERMISSIONS.enums.values())
application = linkedin.LinkedInApplication(authentication)

groups = [(a['group']['id'],a['group']['name']) for a in application.get_memberships(params={'count':'1000'})['values']]

while True:
    group = random.choice(groups)
    #group = (6589270,'test group')
    print group

    #get all posts
    posts = application.get_posts(group[0],params={'count':'10000'})['values']
    posts_id = [(p['id'],p['title']) for p in posts]

    random_post = random.choice(posts_id)
    print posts_id[1]
    comment = raw_input()
    
    if comment.strip():
        application.comment_post(random_post[0], comment)
    

'''
    posts_id = [p['id'] for p in posts]

    #like 10
    c = 10 if len(posts_id) > 10 else len(posts_id)
    for i in range(0,c):
        print 'like %d' % i
        application.like_post(random.choice(posts_id))
        t = random.choice([1,2,3,4])
        time.sleep(t)'''