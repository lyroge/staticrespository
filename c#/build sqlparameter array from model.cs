/// <summary>
/// 根据model对象自动构建一个sqlparameter数组
/// </summary>
/// <param name="procut"></param>
/// <returns></returns>
private List<SqlParameter> BuildSqlParameterArray(object obj, params string[] excludeField)
{
	List<SqlParameter> lsSqlParameter = new List<SqlParameter>();

	FieldInfo[] fieldAry = obj.GetType().GetFields();
	foreach (FieldInfo fi in fieldAry)
	{
		string fieldname = fi.Name;
		if (Array.IndexOf(excludeField, fieldname) == -1)
		{
			lsSqlParameter.Add(new SqlParameter("@"+fieldname, fi.GetValue(obj)));
		}
	}
	return lsSqlParameter;
}