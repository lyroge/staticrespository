/// <summary>
/// 从DataReader绑定到对象属性
/// </summary>
/// <param name="reader"></param>
/// <returns></returns>
private Product BuildProductByDataReader(SqlDataReader reader)
{
	Product p = new Product();
	while (reader.Read())
	{
		int fieldCount = reader.FieldCount;
		for (int i = 0; i < fieldCount; i++)
		{
			//列名
			string fieldName = reader.GetName(i);
			//字段对象
			FieldInfo fi = p.GetType().GetField(fieldName);

			if (fi == null)
				continue;

			//字段类型
			Type fieldType = fi.FieldType;
			//赋值
			if (fi != null)
				fi.SetValue(p, Convert.ChangeType(reader[i], fieldType));
		}
	}
	return p;
}