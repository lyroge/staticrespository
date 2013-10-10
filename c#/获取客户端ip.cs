	private string getIp()
	{
		if (HttpContext.Current.Request.ServerVariables["HTTP_VIA"] != null)
			return HttpContext.Current.Request.ServerVariables["HTTP_X_FORWARDED_FOR"].Split(new[] {','})[0];
		return HttpContext.Current.Request.ServerVariables["REMOTE_ADDR"];
	}