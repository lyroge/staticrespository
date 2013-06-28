/// <summary>
/// 根据model对象自动构建insert sql语句
/// </summary>
/// <param name="procut"></param>
/// <returns></returns>
private string BuildInsertSQL(object obj, params string[] excludeField)
{
	string sql = "insert into {0}({1}) values({2})";
	string tablename = obj.GetType().Name;

	List<string> lsFiled1 = new List<string>();
	List<string> lsFiled2 = new List<string>();

	FieldInfo[] fieldAry = obj.GetType().GetFields();
	foreach (FieldInfo fi in fieldAry)
	{
		string fieldname = fi.Name;
		if (Array.IndexOf(excludeField, fieldname) == -1)
		{
			lsFiled1.Add(fieldname);
			lsFiled2.Add("@" + fieldname);
		}
	}
	return string.Format(sql, tablename, string.Join(",", lsFiled1.ToArray()), string.Join(",", lsFiled2.ToArray()));
}