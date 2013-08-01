
public static DataSet GetList(int PageSize, int PageIndex, string strWhere, string tableName, string keyfield, string ordertype, string fieldlist, string orderfield, DbHelperSQLP DbHelperSQL)
{
	SqlParameter[] parameters = {
		new SqlParameter("@tablename", SqlDbType.VarChar, 255),
	new SqlParameter("@fieldlist", SqlDbType.VarChar,4000),
	  new SqlParameter("@orderfield", SqlDbType.VarChar,100),
		new SqlParameter("@keyfield", SqlDbType.VarChar, 255),
	  new SqlParameter("@pageindex", SqlDbType.Int),
		new SqlParameter("@pagesize", SqlDbType.Int),
	   new SqlParameter("@strWhere", SqlDbType.VarChar,4000),
		new SqlParameter("@ordertype", SqlDbType.VarChar,1)
		};
	parameters[0].Value = tableName;
	parameters[1].Value = fieldlist;
	parameters[2].Value = orderfield;
	parameters[3].Value = keyfield;
	parameters[4].Value = PageIndex;
	parameters[5].Value = PageSize;
	parameters[6].Value = strWhere;
	parameters[7].Value = ordertype;
	string strSql = "";
	if (ordertype == "1")
	{
		strSql = "select top " + PageSize + " " + fieldlist + " from " + tableName + " where " + keyfield + " not in (select top " + PageSize * (PageIndex-1) + " " + keyfield + " from " + tableName + " where 1=1 and " + strWhere + " order by " + orderfield + " desc) and " + strWhere + " order by " + orderfield + " desc";
	}
	else
	{
		strSql = "select top " + PageSize + " " + fieldlist + " from " + tableName + " where " + keyfield + " not in (select top " + PageSize * (PageIndex - 1) + " " + keyfield + " from " + tableName + " where 1=1 and " + strWhere + " order by " + orderfield + " asc) and " + strWhere + " order by " + orderfield + " asc";
	}
	return DbHelperSQL.Query(strSql);
}
