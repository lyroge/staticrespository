urllib.urlopen(url[, data[, proxies]])

###GET Method
urllib.urlopen('http://www.baidu.com/')

###Post Method 
urllib.urlopen('http://www.baidu.com/', 'abc')

###Use Proxy
urllib.urlopen('http://www.baidu.com/', proxies={'http':'http://www.proxy.com:8080'})

###Get A Url Content Copy into a localfile
urllib.urlretrieve(url, filename)

#encode url 
urllib.quote()

#return a=1&b=2
urllib.urlencode({'a':1, 'b':2})

#two UrlOpener
UrlOpener
FancyUrlOpener

###Set a UrlOpener instance , override User-Agent
urllib._urlopener 	
	import urllib
	class AppURLopener(urllib.FancyURLopener):
		version = "App/1.7"
	urllib._urlopener = AppURLopener()