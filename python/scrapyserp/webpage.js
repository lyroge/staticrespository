/*
Date: 2013/12/10
*/

phantom.clearCookies();

var URL = 'http://mall.hongxiu.com/';
var TOTAL_TIME_I = 0.5*60; //30 seconds
var TOTAL_TIME_J = 3.0*60; //180 seconds
var TOTAL_TIME = 0;

x = 0; // current
y = 0; // designed
z = 0; // remain

// generate x between min and max
function random(min,max){
    return Math.floor(min+Math.random()*(max-min));
}

// generate total time seconds
TOTAL_TIME = random(TOTAL_TIME_I,TOTAL_TIME_J);

// generate random stay time seconds
function getRandomStaySeconds(){
	x = random(2,30);
	y += x;
	return y;
}

var sys = require("system");
var webpage = require("webpage");

var page = webpage.create();

ViewPortSize = [];
ViewPortSize[0] = {
  width: 480,
  height: 800
};

ViewPortSize[1] = {
  width: 1024,
  height: 768
};

ViewPortSize[2] = {
  width: 1366,
  height: 768
};

ViewPortSize[3] = {
  width: 1920,
  height: 1024
};

//view port size
page.viewportSize = ViewPortSize[random(0, ViewPortSize.length-1)];

var USER_AGENT_LIST = ['Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1',
'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:14.0) Gecko/20120405 Firefox/14.0a1',
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17',
'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.14 (KHTML, like Gecko) Chrome/24.0.1292.0 Safari/537.14',
'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11',
'Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0',
'Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))',
'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; GTB7.4; InfoPath.2; SV1; .NET CLR 3.3.69573; WOW64; en-US)',
'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; TencentTraveler 4.0; Trident/4.0; SLCC1; Media Center PC 5.0; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30618)',
'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; Maxthon/3.0)']

var ua = USER_AGENT_LIST[random(0, USER_AGENT_LIST.length-1)];

var referer = "http://www.google.com.hk/#newwindow=1&q=free+b2b&safe=strict&start=90";
page.customHeaders = {
  "User-Agent": ua,
  "Accept-Language": "en-US,en;q=0.8",
  "Referer": referer
};

page.onConsoleMessage = function(msg) {
  console.log(msg);
};

phantom.onError = function(msg, trace) {
  console.log('error occur. exit(0)');
  phantom.exit(1);
};

var innerUrl = URL;

console.log(TOTAL_TIME);

console.log('open url:' + innerUrl);
page.open(innerUrl, function(status){
	referer = innerUrl;
	var c = 0;
	var end = random(0, 6);
	for (var ix=0; ix<end; ix++)
	{
		setTimeout(function(){
			c = c + 1;
			page.customHeaders = {
			  "User-Agent": ua,
			  "Accept-Language": "en-US,en;q=0.8",
			  "Referer": referer
			};
			console.log('open url:' + innerUrl);
			page.open(innerUrl, function(status){
				referer = innerUrl;
				page.render(z+'.png')
				z += x;

				innerUrl = page.evaluate(function(){
					function random(min,max){
						return Math.floor(min+Math.random()*(max-min));
					}

					var nodeList = document.getElementsByTagName("a");
					var newurl = "";
					if(nodeList.length==0)
						return newurl;
					while(true){
						newurl = nodeList[random(0, nodeList.length-1)].getAttribute("href");
						if(newurl.indexOf('javascript') == -1){//newurl.indexOf("http://")==0 || newurl[0] == "/"){
							break;
						}
					}
					if (newurl[0] == "/")
						newurl = "http://" + document.domain + newurl;
					else if (newurl.indexOf("http://")!=0){
						var i =document.URL.lastIndexOf('/')
						newurl = document.URL.substring(0,i+1) + newurl;
					}
					return newurl;
				});

				if (c == end || innerUrl==""){
					page.evaluate(function(){
						window.close();
					});
					console.log('exit');
					page.close();
					phantom.exit();
				}
			});
		}, getRandomStaySeconds()*1000);
		console.log(y);
	}
	
	page.render('home.png')

	if (end == 0){
		page.evaluate(function(){
			window.close();
		});
		console.log('exit');
		page.close();
		phantom.exit();
	}
		
	innerUrl = page.evaluate(function(){
		function random(min,max){
			return Math.floor(min+Math.random()*(max-min));
		}

		var nodeList = document.getElementsByTagName("a");
		var newurl = "";
		while(true){
			newurl = nodeList[random(0, nodeList.length-1)].getAttribute("href");
			if(newurl.indexOf('javascript') == -1){
				break;
			}
		}
		if (newurl[0] == "/")
			newurl = "http://" + document.domain + newurl;
		else if (newurl.indexOf("http://")!=0){
			var i =document.URL.lastIndexOf('/')
			newurl = document.URL.substring(0,i+1) + newurl;
		}
		return newurl;
	});
});