# Scrapy settings for robot project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'robot'

SPIDER_MODULES = ['robot.spiders']
NEWSPIDER_MODULE = 'robot.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'robot (+http://www.yourdomain.com)'


DEBUG_REQUEST = False
COOKIES_DEBUG = False
COOKIES_ENABLED = True
LOG_ENABLED = False


DOWNLOAD_DELAY = 8
RANDOMIZE_DOWNLOAD_DELAY = True

DEFAULT_REQUEST_HEADERS ={
     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Accept-Encoding':'gzip,deflate',
     'Referer':'http://www.google.com/',
     'User-Agent':'GoogleBot'
}

DOWNLOADER_MIDDLEWARES = {
    'robot.middleware.logincookie.LoginCookieMiddleware': 101,
}