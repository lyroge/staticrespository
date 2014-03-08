import requests

proxies = {
  "http": "http://186.93.31.168:3128",
  "https": "http://127.0.0.1:8123",
}

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36',
  'Referer': 'http://www.girlgames234.com',
  'Accept-Language': 'zh-CN,zh;q=0.8,de;q=0.6',
 }
r = requests.get('http://www.cpagrip.com/show.php?l=0&u=11436&id=1741&tracking_id=', proxies=proxies, headers=headers)
print r.status_code
