protected override void Render(HtmlTextWriter writer)
{
	StringWriter stringWriter = new StringWriter();
	HtmlTextWriter htmlWriter = new HtmlTextWriter(stringWriter);
	base.Render(htmlWriter);
	string html = stringWriter.ToString();

	html = html.Replace("ctl00_ContentPlaceHolder_Body_", "").Replace("ctl00$ContentPlaceHolder_Body$", "");            
	writer.Write(html);            
}