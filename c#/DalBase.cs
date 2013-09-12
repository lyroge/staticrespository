using System;
using System.Collections.Generic;
using System.Data;
using System.Data.SqlClient;
using System.Reflection;

namespace HongXiu.Mall.DAL
{
    public class MallDalBase
    {
        /// <summary>
        /// SQL 语句缓存
        /// </summary>
        public static Dictionary<string, string> dicSQLCache = new Dictionary<string, string>();

        #region 构造函数 

        public MallDalBase()  { }

        #endregion

        #region 帮助方法

        /// <summary>
        /// 从DataReader自动生成T类型的List
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="reader"></param>
        /// <returns></returns>
        protected List<T> BuildTByDataReader<T>(SqlDataReader reader) where T : new()
        {
            List<T> lsT = new List<T>();

            while (reader.Read())
            {
                T t = new T();
                int fieldCount = reader.FieldCount;

                for (int i = 0; i < fieldCount; i++)
                {
                    //属性对象
                    PropertyInfo fi = t.GetType().GetProperty(reader.GetName(i));
                    if (fi == null)
                        continue;
                    //赋值
                    if (reader[i] != DBNull.Value)
                    {
                        fi.SetValue(t, Convert.ChangeType(reader[i], fi.PropertyType), null);
                    }
                }
                lsT.Add(t);
            }
            reader.Close();
            return lsT;
        }

        #region 构建SQL语句相关

        /// <summary>
        /// 根据model对象自动构建一个sqlparameter数组
        /// </summary>
        /// <param name="procut"></param>
        /// <returns></returns>
        protected List<SqlParameter> BuildSqlParameterArray(object obj, params string[] excludeField)
        {
            List<SqlParameter> lsSqlParameter = new List<SqlParameter>();

            PropertyInfo[] fieldAry = obj.GetType().GetProperties();
            foreach (PropertyInfo fi in fieldAry)
            {
                string fieldname = fi.Name;
                if (Array.IndexOf(excludeField, fieldname) == -1)
                {
                    object val = fi.GetValue(obj, null);
                    //特殊的值进行处理
                    if (fi.PropertyType == typeof(DateTime) && Convert.ToDateTime(val) == DateTime.MinValue)
                        val = DBNull.Value;
                    lsSqlParameter.Add(new SqlParameter("@" + fieldname, val));
                }
            }
            return lsSqlParameter;
        }

        /// <summary>
        /// 根据model对象自动构建insert sql语句
        /// </summary>
        /// <param name="procut"></param>
        /// <returns></returns>
        protected string BuildInsertSQL(object obj, params string[] excludeField)
        {
            string key = string.Format("INSERT_SQL_OBJECT-{0}_EXCLUDEFIELD-{1}", obj.ToString(), string.Join("-", excludeField));
            if (dicSQLCache.ContainsKey(key))
                return dicSQLCache[key];

            string sql = "insert into [{0}]({1}) values({2})";
            string tablename = obj.GetType().Name;

            List<string> lsFiled1 = new List<string>();
            List<string> lsFiled2 = new List<string>();

            PropertyInfo[] fieldAry = obj.GetType().GetProperties();
            foreach (PropertyInfo fi in fieldAry)
            {
                string fieldname = fi.Name;
                if (Array.IndexOf(excludeField, fieldname) == -1)
                {
                    lsFiled1.Add(fieldname);
                    lsFiled2.Add("@" + fieldname);
                }
            }
            sql = string.Format(sql, tablename, string.Join(",", lsFiled1.ToArray()), string.Join(",", lsFiled2.ToArray()));
            dicSQLCache[key] = sql;
            return sql;
        }

        /// <summary>
        /// 根据model对象自动构建update sql语句
        /// </summary>
        /// <param name="procut"></param>
        /// <returns></returns>
        protected string BuildUpdateSQL(object obj, params string[] excludeField)
        {
            return BuildUpdateSQL("ID", obj, excludeField);
        }

        /// <summary>
        /// 根据model对象自动构建update sql语句
        /// </summary>
        /// <param name="procut"></param>
        /// <returns></returns>
        protected string BuildUpdateSQL(string idname, object obj, params string[] excludeField)
        {
            string key = string.Format("UPDATE_SQL_OBJECT-{0}_IDNAME-{1}_EXCLUDEFIELD-{2}", obj.ToString(), idname, string.Join("-", excludeField));
            if (dicSQLCache.ContainsKey(key))
                return dicSQLCache[key];

            string sql = "update [{0}] set {1} where {2}=@{2}";
            string tablename = obj.GetType().Name;

            List<string> lsFiled1 = new List<string>();

            PropertyInfo[] fieldAry = obj.GetType().GetProperties();
            foreach (PropertyInfo fi in fieldAry)
            {
                string fieldname = fi.Name;
                if (Array.IndexOf(excludeField, fieldname) == -1 && fieldname != idname)
                {
                    lsFiled1.Add(fieldname + "=@" + fieldname);
                }
            }
            sql = string.Format(sql, tablename, string.Join(",", lsFiled1.ToArray()), idname);
            dicSQLCache[key] = sql;
            return sql;
        }


        #endregion

        #endregion

        #region GetByID

        public T GetByID<T>(int id) where T : class, new()
        {
            return GetByID<T>("id", id);
        }

        public T GetByID<T>(string idname, int id) where T : class, new()
        {
            string tablename = typeof(T).Name;
            SqlDataReader reader = DbHelperSQL.ExecuteReader(string.Format("select * from [{0}] where {2} = {1}", tablename, id, idname));
            List<T> ls = BuildTByDataReader<T>(reader);
            T t = ls.Count == 0 ? null : ls[0];
            return t;
        }

        #endregion

        #region DelByID

        public bool DelByID<T>(int id)
        {
            return DelByID<T>("id", id);
        }

        public bool DelByID<T>(string idname, int id)
        {
            string tablename = typeof(T).Name;
            return ExecuteSql(string.Format("delete from [{0}] where {2} = {1}", tablename, id, idname));
        }

        #endregion

        #region AddByObj

        public bool AddByObj<T>(T t, params string[] excludeField) where T : new()
        {
            List<SqlParameter> ls = BuildSqlParameterArray(t, excludeField);
            return ExecuteSql(BuildInsertSQL(t, excludeField), ls.ToArray());
        }

        public int AddByObj_ReturnInsertID<T>(T t, params string[] excludeField) where T : new()
        {
            List<SqlParameter> ls = BuildSqlParameterArray(t);
            object obj = DbHelperSQL.GetSingle(BuildInsertSQL(t, excludeField) + ";select @@IDENTITY", ls.ToArray());
            return Convert.ToInt32(obj);
        }

        #endregion

        #region UpdateByObj

        public bool UpdateByObj<T>(T t, params string[] excludeField) where T : new()
        {
            return UpdateByObj<T>("ID", t, excludeField);
        }

        public bool UpdateByObj<T>(string idname, T t, params string[] excludeField) where T : new()
        {
            string sql = BuildUpdateSQL(idname, t, excludeField);
            List<SqlParameter> ls = BuildSqlParameterArray(t, excludeField);
            return ExecuteSql(sql, ls.ToArray());
        }

        #endregion

        #region GetListBySQL

        public DataTable GetListBySQL(string sql)
        {
            return DbHelperSQL.Query(sql).Tables[0];
        }

        public List<T> GetObjListBySQL<T>(string sql) where T : new()
        {
            SqlDataReader reader = DbHelperSQL.ExecuteReader(sql);
            return BuildTByDataReader<T>(reader);
        }

        public DataSet GetDataSetBySQL(string sql)
        {
            return DbHelperSQL.Query(sql);
        }

        #endregion

        #region ExecuteSql

        public bool ExecuteSql(string sql, params SqlParameter[] aryParam)
        {
            return DbHelperSQL.ExecuteSql(sql, aryParam) != -1;
        }

        #endregion

        #region 纯sql语句

        #region 更新

        public bool Update(string tablename, string idname, string id, Dictionary<string, object> kv)
        {
            string sql = "update {0} set {1} where {2}={3}";

            List<string> lsFieldName = new List<string>();
            List<SqlParameter> lsParameter = new List<SqlParameter>();

            foreach (KeyValuePair<string, object> o in kv)
            {
                lsFieldName.Add(string.Format("{0}=@{0}", o.Key));
                lsParameter.Add(new SqlParameter("@" + o.Key, o.Value));
            }
            return ExecuteSql(string.Format(sql, tablename, string.Join(",", lsFieldName.ToArray()), idname, id), lsParameter.ToArray());
        }

        public bool Update(string tablename, string id, Dictionary<string, object> kv)
        {
            return Update(tablename, "id", id, kv);
        }

        #endregion

        #region 添加

        public bool Insert(string tablename, Dictionary<string, object> kv)
        {
            string sql = "insert {0}({1}) values({2})";

            List<string> lsFieldName = new List<string>();
            List<string> lsFieldValue = new List<string>();
            List<SqlParameter> lsParameter = new List<SqlParameter>();

            foreach (KeyValuePair<string, object> o in kv)
            {
                lsFieldName.Add(o.Key);
                lsFieldValue.Add("@" + o.Key);
                lsParameter.Add(new SqlParameter("@" + o.Key, o.Value));
            }
            return ExecuteSql(string.Format(sql, tablename, string.Join(",", lsFieldName.ToArray()), string.Join(",", lsFieldValue.ToArray())), lsParameter.ToArray());
        }

        #endregion

        #region 删除

        public bool Delete(string tablename, string idname, string id)
        {
            return ExecuteSql(string.Format("delete from {0} where {1} = {2}", tablename, idname, id));
        }

        public bool Delete(string tablename, string id)
        {
            return ExecuteSql(string.Format("delete from {0} where id = {1}", tablename, id));
        }

        #endregion

        #endregion


        #region 分页获取数据列表 GetList

        public DataTable GetListByPageIndex(int pageSize, int pageIndex, string idName, string tableName, string fieldList, string where, string orderField, string orderType)
        {
            SqlParameter[] parameters =             
            {
                new SqlParameter("@tableName", tableName),
                new SqlParameter("@fieldList", fieldList),
                new SqlParameter("@orderField", orderField),
                new SqlParameter("@idName", idName),
                new SqlParameter("@pageIndex", pageIndex),
                new SqlParameter("@pageSize", pageSize),
                new SqlParameter("@where", where),
                new SqlParameter("@orderType", orderType)
            };
            string sql =
            "select top @pageSize @fieldList from @tableName where @idName not in (select top @pageSize * (@pageIndex - 1) @idName from @tableName where 1=1 @where order by @orderField @orderType) and @where order by @orderField @orderType";

            return DbHelperSQL.Query(sql, parameters).Tables[0];
        }

        #endregion

    }
}
