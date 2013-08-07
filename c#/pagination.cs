/// <summary>
/// 生成页码
/// </summary>
/// <param name="thisPage"></param>
private void getPageHtml(int pageIndex, int recordcount)
{
	//不够一页
	if (recordcount <= PageSize)
		return;

	if (pageIndex == 0)
		pageIndex = 1;
	
	string _url = HttpContext.Current.Request.Url.PathAndQuery.ToString();
	Regex regex = new Regex("page=[0-9]+");
	if (regex.IsMatch(_url))
	{
		string pagestr = regex.Match(_url).Groups[0].Value;
		_url = _url.Replace(pagestr, "page=");
	}
	else
	{
		_url +=  (_url.Contains("?") ? "&" : "?") + "page="; }


	//分页逻辑代码 计算开始、结束页码
	int pagecount = (int)Math.Ceiling(recordcount / (PageSize * 1.0));//总页数
	int start = 1, end = pagecount>10?10 : pagecount;
	bool isendpagenum = false;
	if (pageIndex > 5)
	{
		if (pageIndex + 5 < pagecount)
		{
			end = pageIndex + 5;
			start = pageIndex - 4;
		}
		else
		{
			end = pagecount;
			if (pagecount < 10)
				start = 1;
			else
				start = pagecount - 9;
			isendpagenum = true;
		}
	}


	StringBuilder sb = new StringBuilder();

	//输出首页码
	if (pageIndex > 5  && pagecount > 10)
		sb.AppendLine("<a href='" + _url + "1' >1</a>...");

	for (int i = start; i < end + 1; i++)
	{
		if (i == pageIndex)
		{
			sb.AppendLine("<span style='margin-right:5px;font-weight:Bold;color:red;'>" + pageIndex + "</span>");
			continue;
		}
		sb.AppendLine("<a href='" + _url + i.ToString() + "' >"+i.ToString()+"</a>");
	}
	if (!isendpagenum && pagecount > 10)
		sb.AppendLine("...<a href='" + _url + pagecount.ToString() + "' >" + pagecount.ToString() + "</a>");

	sb.AppendLine("<a href='" + _url + (pageIndex + 1).ToString() + "'>下一页</a>");
	sb.AppendLine("转到<input type='text' value='" + pageIndex.ToString() + "' name='PagerInput' id='PagerInput' style='width:30px;' />页<input type='Button' name='AspNetPager1' id='AspNetPager1_btn' value='Go' onclick=\"javascript:jumpto(document.getElementById('PagerInput').value);\" />");

	this.htmlpage.InnerHtml = sb.ToString();
}
