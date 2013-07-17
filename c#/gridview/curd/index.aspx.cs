#region 编辑事件

protected void GridView1_RowDeleting(object sender, GridViewDeleteEventArgs e)
{
    int index = e.RowIndex;//获取当前行的索引  
    int id = Convert.ToInt32((this.GridView1.Rows[index].FindControl("Label1") as Label).Text);
    bool b = dal.DeleteTjProduct(id);
    if (b)
    {
        Response.Write("<script>alert('删除成功！')</script>");
        GetData();
    }
    else
    {
        Response.Write("<script>alert('删除失败！')</script>");
    }
}

protected void GridView1_RowDataBound(object sender, GridViewRowEventArgs e)
{
    if (e.Row.RowType == DataControlRowType.DataRow)
    {
        LinkButton lb = e.Row.FindControl("LinkButton2") as LinkButton;
        if (lb.Text == "删除")
        {
            lb.Attributes.Add("onclick", "return confirm('确定要删除这一行吗？')");
        }
    }
}

protected void GridView1_RowEditing(object sender, GridViewEditEventArgs e)
{
    GridView1.EditIndex = e.NewEditIndex;
    GetData();
}

protected void GridView1_RowCancelingEdit(object sender, GridViewCancelEditEventArgs e)
{
    GridView1.EditIndex = -1;
    GetData();
}

protected void GridView1_RowUpdating(object sender, GridViewUpdateEventArgs e)
{
    int id = Convert.ToInt32((this.GridView1.Rows[e.RowIndex].FindControl("Label1") as Label).Text);

    string productcode = (GridView1.Rows[e.RowIndex].FindControl("TextBox2") as TextBox).Text;
    string tjtitle = (GridView1.Rows[e.RowIndex].FindControl("TextBox3") as TextBox).Text;
    bool b = dal.UpdateTjProduct(id, productcode, tjtitle);
    if (b)
    {
        Response.Write("<script>alert('更新成功！')</script>");
        GridView1.EditIndex = -1;
        GetData();
    }
    else
    {
        Response.Write("<script>alert('更新失败！')</script>");
    }
}

#endregion
