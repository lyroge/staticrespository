using System;
using System.Collections.Generic;
using System.Text;
using System.Data.SqlClient;
using System.Reflection;
using System.Web;
using System.Data;

namespace HongXiu.Mall.DAL
{
    public class MallDalBase
    {
        #region 帮助方法

        /// <summary>
        /// 从DataReader自动生成T类型的List
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="reader"></param>
        /// <returns></returns>
        protected List<T> BuildTByDataReader<T>(SqlDataReader reader) where T: new()
        {
            List<T> lsT = new List<T>();

            while (reader.Read())
            {
                T t = new T();
                int fieldCount = reader.FieldCount;
                for (int i = 0; i < fieldCount; i++)
                {
                    //列名
                    string fieldName = reader.GetName(i);

                    //字段对象
                    FieldInfo fi = t.GetType().GetField(fieldName);

                    if (fi == null)
                        continue;

                    //字段类型
                    Type fieldType = fi.FieldType;

                    //赋值
                    if (reader[i] != DBNull.Value)
                        fi.SetValue(t, Convert.ChangeType(reader[i], fieldType));
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

            FieldInfo[] fieldAry = obj.GetType().GetFields();
            foreach (FieldInfo fi in fieldAry)
            {
                string fieldname = fi.Name;
                if (Array.IndexOf(excludeField, fieldname) == -1)
                {
                    lsSqlParameter.Add(new SqlParameter("@" + fieldname, fi.GetValue(obj)));
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

        /// <summary>
        /// 根据model对象自动构建update sql语句
        /// </summary>
        /// <param name="procut"></param>
        /// <returns></returns>
        protected string BuildUpdateSQL(object obj, int id, params string[] excludeField)
        {
            string sql = "update {0} set {1} where id={2}";
            string tablename = obj.GetType().Name;

            List<string> lsFiled1 = new List<string>();

            FieldInfo[] fieldAry = obj.GetType().GetFields();
            foreach (FieldInfo fi in fieldAry)
            {
                string fieldname = fi.Name;
                if (Array.IndexOf(excludeField, fieldname) == -1)
                {
                    lsFiled1.Add(fieldname + "=@" + fieldname);
                }
            }
            return string.Format(sql, tablename, string.Join(",", lsFiled1.ToArray()), id);
        }

        #endregion

        #endregion

        /// <summary>
        /// 根据ID获取对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="id"></param>
        /// <returns></returns>
        public T GetByID<T>(int id) where T : class, new()
        {
            string tablename = typeof(T).Name;
            SqlDataReader reader = DbHelperSQL.ExecuteReader(string.Format("select * from [{0}] where id = {1}", tablename, id));
            List<T> ls = BuildTByDataReader<T>(reader);
            T t = ls.Count == 0 ? null : ls[0];
            return t;
        }

        /// <summary>
        /// 根据ID删除记录
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="id"></param>
        /// <returns></returns>
        public bool DelByID<T>(int id)
        {
            string tablename = typeof(T).Name;
            return DbHelperSQL.ExecuteSql(string.Format("delete from [{0}] where id = {1}", tablename, id)) != -1;
        }

        /// <summary>
        /// 添加一个对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="t"></param>
        /// <param name="excludeField"></param>
        /// <returns></returns>
        public bool AddByObj<T>(T t, params string[] excludeField) where T : new()
        {
            List<SqlParameter> ls = BuildSqlParameterArray(t);
            return DbHelperSQL.ExecuteSql(BuildInsertSQL(t, excludeField), ls.ToArray()) != -1;
        }

		/// <summary>
        /// 添加一个对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="t"></param>
        /// <param name="excludeField"></param>
        /// <returns></returns>
        public int AddByObj_ReturnInsertID<T>(T t, params string[] excludeField) where T : new()
        {
            List<SqlParameter> ls = BuildSqlParameterArray(t);
            object obj = DbHelperSQL.GetSingle(BuildInsertSQL(t, excludeField) +";select @@IDENTITY", ls.ToArray());
            int id = -1;
            return Convert.ToInt32(obj);
        }

        /// <summary>
        /// 更新一个对象
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="t"></param>
        /// <returns></returns>
        public bool UpdateByObj<T>(T t, params string[] excludeField) where T : new()
        {
            int id = Convert.ToInt32(t.GetType().GetField("ID").GetValue(t));
            string sql = BuildUpdateSQL(t, id,excludeField);
            List<SqlParameter> ls = BuildSqlParameterArray(t, excludeField);
            return DbHelperSQL.ExecuteSql(sql, ls.ToArray()) != -1;
        }

        /// <summary>
        /// 获取一个DataTable数据集
        /// </summary>
        /// <param name="sql"></param>
        /// <returns></returns>
        public DataTable GetListBySQL(string sql)
        {
            return DbHelperSQL.Query(sql).Tables[0];
        }

        /// <summary>
        /// 执行insert、delte、update操作
        /// </summary>
        /// <param name="sql"></param>
        /// <returns></returns>
        public bool ExecuteSql(string sql)
        {
            return DbHelperSQL.ExecuteSql(sql) != -1;
        }

        /// <summary>
        /// 获取对象类型的列表
        /// </summary>
        /// <param name="sql"></param>
        /// <returns></returns>
        public List<T> GetObjListBySQL<T>(string sql) where T : new()
        {
            SqlDataReader reader = DbHelperSQL.ExecuteReader(sql);
            return BuildTByDataReader<T>(reader);
        }
    }
}
