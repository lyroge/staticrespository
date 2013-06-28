/// <summary>
/// 从request中获取值自动绑定到对象
/// </summary>
/// <returns></returns>
Product BuildProdctFromRequest()
{
	string[] keyAry = Request.Form.AllKeys;

	Product p = new Product();
	foreach (string key in keyAry)
	{
		//获取指定字段
		FieldInfo fi  = p.GetType().GetField(key);
		if (fi != null)
		{
			if (string.IsNullOrEmpty(Request.Form[key]) == false)
			{
				//字段类型
				Type t = fi.FieldType;

				//设置字段值， 自动转换类型
				fi.SetValue(p, Convert.ChangeType(Request.Form[key], t));
			}
		}
	}
	return p;
}