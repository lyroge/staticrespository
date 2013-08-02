HttpWebRequest request = null;
HttpWebResponse response = null;

string Cookiesstr = string.Empty;

//第一次POST请求
string postdata = "a=b&c=3";//模拟请求数据
request = (HttpWebRequest)WebRequest.Create("posturl");//实例化web访问类
request.Method = "POST";//数据提交方式为POST
//模拟头
request.ContentType = "application/x-www-form-urlencoded";
byte[] postdatabytes = Encoding.GetEncoding("gb2312").GetBytes(postdata);
request.ContentLength = postdatabytes.Length;
request.AllowAutoRedirect = true;
request.CookieContainer = cc;
request.KeepAlive = true;
//提交请求
Stream stream = request.GetRequestStream();
stream.Write(postdatabytes, 0, postdatabytes.Length);
stream.Close();
//接收响应
response = (HttpWebResponse)request.GetResponse();
//保存返回cookie
string strcrook = request.CookieContainer.GetCookieHeader(request.RequestUri);
Cookiesstr = strcrook;
response.Close();

request = (HttpWebRequest)WebRequest.Create("get url");
request.Method = "GET";
request.KeepAlive = true;
request.Headers.Add("Cookie:" + Cookiesstr);
request.CookieContainer = cc;
request.AllowAutoRedirect = false;
response = (HttpWebResponse)request.GetResponse();
StreamReader sr1 = new StreamReader(response.GetResponseStream(), true);
string ss1 = sr1.ReadToEnd();
sr1.Close();
response.Close();

JavaScriptObject loginObject = JavaScriptConvert.DeserializeObject(ss1) as JavaScriptObject;
JavaScriptObject obj = loginObject["data"] as JavaScriptObject;
obj = obj["list"] as JavaScriptObject;
JavaScriptArray ary = obj["items"] as JavaScriptArray;
foreach (JavaScriptObject a in ary)
{
	string siteid = a["siteid"].ToString();
	string ypv = a["y_pv"].ToString();
	string query = a["query"].ToString();
	if (dicSiteNameSiteID.ContainsKey(int.Parse(siteid)))
	{
	}
}