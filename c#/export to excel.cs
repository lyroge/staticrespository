protected void BtnExcel_Click(object sender, EventArgs e)
{
	Response.AppendHeader("Content-Disposition",string.Format("attachments;filename={0}",HttpUtility.UrlEncode("abc.xls", Encoding.UTF8).ToString()));
	Response.ContentType = "application/ms-excel";
	EnableViewState = false;

	StringWriter writer = new StringWriter();
	HtmlTextWriter hw = new HtmlTextWriter(writer);
	Repeater1.RenderControl(hw);
	Response.Write(writer.ToString());
	Response.End();
}