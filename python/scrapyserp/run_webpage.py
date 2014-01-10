import os
from random import choice

with open('proxy/proxies.txt') as f:
	ip_port_list = f.readlines()
	ip_port = choice(ip_port_list)[7:-1]
	print ip_port
	cmd =  'phantomjs --proxy=%s webpage.js' % (ip_port,)
	os.system(cmd)