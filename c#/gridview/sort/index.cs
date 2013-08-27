
		
		
		
		
		
		
		
	protected void GridView1_Sorting(object sender, GridViewSortEventArgs e)
        {
            string sPage = e.SortExpression;
            if (sPage == ViewState["sortfield"].ToString())
            {
                if (ViewState["sortdir"].ToString() == "desc")
                    ViewState["sortdir"] = "asc";
                else
                    ViewState["sortdir"] = "desc";
            }
            else
            {
                ViewState["sortfield"] = sPage;
                ViewState["sortdir"] = "desc";
            }
            Bind();
        }