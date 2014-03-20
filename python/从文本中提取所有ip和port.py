# -- coding:utf-8 --

s = '''
Free Proxy List
Google
Https
Last Checked
							
190.204.23.139	8080	VE	Venezuela	anonymous	no	yes	7 seconds ago
201.209.100.238	8080	VE	Venezuela	anonymous	no	yes	7 seconds ago
190.206.27.24	8080	VE	Venezuela	anonymous	no	yes	7 seconds ago
210.0.201.162	80	HK	Hong Kong	elite proxy	no	no	8 seconds ago
186.95.3.226	8080	VE	Venezuela	anonymous	no	yes	8 seconds ago
190.199.55.233	8080	VE	Venezuela	anonymous	no	no	9 seconds ago
201.242.106.131	8080	VE	Venezuela	anonymous	no	no	9 seconds ago
190.204.100.40	8080	VE	Venezuela	anonymous	yes	yes	9 seconds ago
190.75.109.241	8080	VE	Venezuela	anonymous	no	no	9 seconds ago
190.39.57.13	8080	VE	Venezuela	anonymous	yes	yes	9 seconds ago
202.175.83.61	1234	MO	Macau	elite proxy	no	no	9 seconds ago
203.172.222.238	8080	TH	Thailand	anonymous	no	no	9 seconds ago
212.107.116.234	443	SA	Saudi Arabia	anonymous	no	no	9 seconds ago
190.204.232.62	8080	VE	Venezuela	anonymous	no	yes	9 seconds ago
201.242.88.55	8080	VE	Venezuela	anonymous	no	no	9 seconds ago
190.204.97.65	8080	VE	Venezuela	anonymous	yes	yes	1 minute ago
186.89.64.233	8080	VE	Venezuela	anonymous	yes	yes	1 minute ago
201.242.64.82	8080	VE	Venezuela	anonymous	yes	yes	1 minute ago
190.73.199.24	8080	VE	Venezuela	anonymous	yes	yes	1 minute ago
190.75.224.180	8080	VE	Venezuela	anonymous	yes	yes	1 minute ago
Showing 1 to 20 of 300 entriesFirstPrevious12345NextLast
How to use the proxy?
All the browsers (chrome, firefox, ie, opera, safari and others) support the proxy option. When you set a proxy in browser, the proxy will fetch the web pages for your browser. The webistes regard the IP of proxy as your IP so it cannot trace your real IP. We recommend using Elite Proxy Switcher to set the proxy for your browsers.
What is the proxy anonymity?
There are 3 levels of proxies according to their anonymity.
'''

import re
reg = re.compile('(\d+\.\d+\.\d+\.\d+).*?(\d+)', re.U)

result = reg.findall(s)
for ip,port in result:
	print "%s:%s" % (ip,port)